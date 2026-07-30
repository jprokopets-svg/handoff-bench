#!/usr/bin/env python3
"""
handoff_v2.py — Handoff Study V2.

8 hard tasks x 5 conditions x 3 seeds = 120 runs. Budget ~$12.

Conditions:
  RAW       — A's full transcript (tool calls + results) to B
  BRIEF     — A writes structured briefing, max 400 completion tokens
  WAKE      — WAKE-style briefing: goal / state / belief+confidence /
              broken / next action / warning
  NO-HANDOFF — B gets spec + file state only
  CONTINUOUS — one agent, 12 uninterrupted turns (ceiling)

Hard tasks target 40-70% continuous pass rate.
Interrupt at turn 7 / 12-turn budget.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "calib-bench" / "src"))
from pipeline import generate, generate_chat

# ---------------------------------------------------------------------------
# 8 hard problems (code-hard tier + harder)
# ---------------------------------------------------------------------------

HARD_PROBLEMS = [
    {
        "name": "regex_parser",
        "prompt": "Write a function that determines if a given string matches a simple pattern language: '.' matches any char, '*' matches zero or more of preceding char. Implement basic regex matching without using the re module.",
        "func_sig": "def is_match(s: str, p: str) -> bool:",
        "tests": [
            "assert is_match('aa', 'a') == False",
            "assert is_match('aa', 'a*') == True",
            "assert is_match('ab', '.*') == True",
            "assert is_match('aab', 'c*a*b') == True",
            "assert is_match('mississippi', 'mis*is*p*.') == False",
            "assert is_match('', '.*') == True",
        ],
    },
    {
        "name": "n_queens",
        "prompt": "Write a function that returns all distinct solutions to the N-Queens problem. Each solution is a list of strings where 'Q' marks a queen and '.' marks empty.",
        "func_sig": "def solve_n_queens(n: int) -> list[list[str]]:",
        "tests": [
            "assert len(solve_n_queens(4)) == 2",
            "assert len(solve_n_queens(1)) == 1",
            "assert all(len(row) == 4 for sol in solve_n_queens(4) for row in sol)",
            "assert all(row.count('Q') == 1 for sol in solve_n_queens(4) for row in sol)",
        ],
    },
    {
        "name": "median_stream",
        "prompt": "Write a class that maintains the median of a stream of numbers as they arrive. Support add_num and find_median operations with O(log n) add and O(1) find.",
        "func_sig": "class MedianFinder:",
        "tests": [
            "mf = MedianFinder(); mf.add_num(1); mf.add_num(2); assert mf.find_median() == 1.5",
            "mf = MedianFinder(); mf.add_num(1); assert mf.find_median() == 1.0",
            "mf = MedianFinder(); mf.add_num(1); mf.add_num(2); mf.add_num(3); assert mf.find_median() == 2.0",
        ],
    },
    {
        "name": "word_break",
        "prompt": "Write a function that determines if a string can be segmented into space-separated words from a given dictionary.",
        "func_sig": "def word_break(s: str, word_dict: list[str]) -> bool:",
        "tests": [
            "assert word_break('leetcode', ['leet','code']) == True",
            "assert word_break('applepenapple', ['apple','pen']) == True",
            "assert word_break('catsandog', ['cats','dog','sand','and','cat']) == False",
            "assert word_break('', ['a']) == True",
        ],
    },
    {
        "name": "median_two_sorted",
        "prompt": "Write a function that finds the median of two sorted arrays in O(log(min(m,n))) time.",
        "func_sig": "def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:",
        "tests": [
            "assert find_median_sorted_arrays([1,3], [2]) == 2.0",
            "assert find_median_sorted_arrays([1,2], [3,4]) == 2.5",
            "assert find_median_sorted_arrays([0,0], [0,0]) == 0.0",
            "assert find_median_sorted_arrays([], [1]) == 1.0",
        ],
    },
    {
        "name": "serialize_tree",
        "prompt": "Write functions to serialize a binary tree to a string and deserialize it back. Use level-order traversal with 'null' for missing nodes.",
        "func_sig": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef serialize(root: TreeNode | None) -> str: ...\ndef deserialize(data: str) -> TreeNode | None: ...",
        "tests": [
            "root = deserialize('[1,2,3,null,null,4,5]'); assert serialize(root) == '[1,2,3,null,null,4,5]'",
            "root = deserialize('[]'); assert serialize(root) == '[]'",
            "root = deserialize('[1]'); assert serialize(root) == '[1]'",
        ],
    },
    {
        "name": "max_path_sum",
        "prompt": "Write a function that finds the maximum path sum in a binary tree. A path can start and end at any node.",
        "func_sig": "def max_path_sum(root: TreeNode | None) -> int:",
        "tests": [
            "n = TreeNode(1, TreeNode(2), TreeNode(3)); assert max_path_sum(n) == 6",
            "n = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7))); assert max_path_sum(n) == 42",
            "n = TreeNode(-3); assert max_path_sum(n) == -3",
        ],
    },
    {
        "name": "merge_k_lists",
        "prompt": "Write a function that merges k sorted linked lists into one sorted list. Each list node has val and next attributes.",
        "func_sig": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:",
        "tests": [
            "def ll(vals):\n    if not vals: return None\n    head = ListNode(vals[0])\n    cur = head\n    for v in vals[1:]:\n        cur.next = ListNode(v)\n        cur = cur.next\n    return head\n\ndef to_list(n):\n    r = []\n    while n:\n        r.append(n.val)\n        n = n.next\n    return r\n\nassert to_list(merge_k_lists([ll([1,4,5]), ll([1,3,4]), ll([2,6])])) == [1,1,2,3,4,4,5,6]",
            "assert merge_k_lists([]) is None",
            "assert to_list(merge_k_lists([ll([1])])) == [1]",
        ],
    },
]

MODEL = "anthropic/claude-haiku-4.5"
SEEDS = [42, 123, 256]
TURNS_A = 7
TURNS_B = 5  # 12 total - 7
TURNS_ALL = 12
VENV_PYTHON = str(Path(__file__).resolve().parent / ".venv" / "bin" / "python3")

TOOLS = [
    {"type": "function", "function": {
        "name": "read_file", "description": "Read a file from the workspace",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "write_file", "description": "Write content to a file",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
    {"type": "function", "function": {
        "name": "run_tests", "description": "Run pytest on the solution file",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "finish", "description": "Submit the current solution and stop",
        "parameters": {"type": "object", "properties": {}}}},
]

SYSTEM_PROMPT_TEMPLATE = """You are an AI coding assistant. You have access to a Python workspace.

Your task: Write a correct solution function in {entry_file}.py. The test file is test_{entry_file}.py.

CRITICAL: You MUST write code. Reading files alone does nothing. Follow this protocol exactly:

1. Read the test file ONCE to understand what's expected (or read the current solution file).
2. IMMEDIATELY write a solution to {entry_file}.py using write_file.
3. Run tests with run_tests().
4. If tests fail, fix your code with write_file and test again.
5. Call finish() when all tests pass.

Do not read files more than once. Writing and testing is how you make progress.
You have a maximum of {max_turns} turns."""

BRIEF_PROMPT = """You are being interrupted mid-task. Write a BRIEFING for the next agent. Maximum 400 tokens.

Use this format:
GOAL: <what the task requires>
STATE: <what exists so far>
DONE: <what is working>
BROKEN: <what is failing or unknown>
NEXT: <the single most important thing to try>

Current code in {entry_file}.py:
```
{code}
```

Test results:
{test_results}

Write your briefing (max 400 tokens):"""

WAKE_PROMPT = """You are being interrupted mid-task. Write a WAKE briefing — the format I use to brief myself between sessions.

Maximum 500 tokens. Use this structure:
GOAL: <one-line task statement>
STATE: <current state of work, what files exist, what's been tried>
BELIEF: <what I believe is the right approach and how confident I am (0-100%)>
BROKEN: <what's failing and why I think it's failing>
NEXT: <the next thing I would do if I were continuing>
WARNING: <the thing I'm most worried about / the gotcha I discovered>

Current code in {entry_file}.py:
```
{code}
```

Test results:
{test_results}

Write your WAKE briefing (max 500 tokens):"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def setup_workspace(prob: dict, work_dir: Path):
    work_dir.mkdir(parents=True, exist_ok=True)
    entry_file = work_dir / f"{prob['name']}.py"
    if entry_file.exists():
        entry_file.unlink()
    # Write the full func_sig as a stub with pass/... bodies
    sig = prob['func_sig']
    # For multi-line sigs (class + functions), generate proper stub
    if '\n' in sig:
        lines = sig.split('\n')
        stub_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('class '):
                stub_lines.append(line)
                stub_lines.append('    pass')
            elif stripped.startswith('def '):
                stub_lines.append(line)
                stub_lines.append('    ...')
            elif stripped == '':
                stub_lines.append('')
            else:
                stub_lines.append(line)
        entry_file.write_text('\n'.join(stub_lines) + '\n')
    else:
        entry_file.write_text(f"{sig}\n    pass\n")
    # Tests
    test_path = work_dir / f"test_{prob['name']}.py"
    test_code = "\n".join([
        f"from {prob['name']} import *",
        "",
        *[f"\n{t}" for t in prob["tests"]],
    ])
    test_path.write_text(test_code)
    return entry_file


def read_file_content(work_dir: Path, filename: str) -> str:
    if not filename or filename.strip() in ("/", "."):
        return f"ERROR: invalid path '{filename}'"
    path = work_dir / filename
    if path.exists() and path.is_file():
        return path.read_text()
    return f"ERROR: file not found: {filename}"


def write_file_content(work_dir: Path, filename: str, content: str):
    (work_dir / filename).write_text(content)
    return f"Written to {filename}"


def run_pytest(work_dir: Path) -> str:
    python = VENV_PYTHON if Path(VENV_PYTHON).exists() else "python3"
    result = subprocess.run(
        [python, "-m", "pytest", str(work_dir), "-v", "--tb=short", "-q"],
        capture_output=True, text=True, timeout=30
    )
    output = result.stdout + result.stderr
    return output[-2000:] if len(output) > 2000 else output


def grade_task(work_dir: Path) -> bool:
    python = VENV_PYTHON if Path(VENV_PYTHON).exists() else "python3"
    result = subprocess.run(
        [python, "-m", "pytest", str(work_dir), "-q", "--tb=no"],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0


def count_completion_tokens(raw_response: str) -> int:
    """Rough estimate: 1 token ≈ 4 characters for English text."""
    return len(raw_response) // 4


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

def run_agent(prob, init_context, max_turns, work_dir, seed, store_log=True):
    entry_file = prob["name"]
    work_dir.mkdir(parents=True, exist_ok=True)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_TEMPLATE.format(entry_file=entry_file, max_turns=max_turns)},
        {"role": "user", "content": init_context},
    ]
    turn_log = []
    for turn in range(1, max_turns + 1):
        response_text, tokens_used = generate_chat(MODEL, messages, temperature=0.3, max_tokens=4096, tools=TOOLS, seed=seed)
        entry = {"turn": turn, "response": response_text, "tokens": tokens_used}

        if response_text.startswith('{"__tool_calls__"'):
            messages.append({"role": "assistant", "content": response_text})
            tc_data = json.loads(response_text)
            tool_calls = tc_data.get("__tool_calls__", [])
        else:
            messages.append({"role": "assistant", "content": response_text})
            tool_calls = []

        for tc in tool_calls:
            fn_name = tc.get("function", {}).get("name", "")
            fn_args_r = tc.get("function", {}).get("arguments", "{}")
            fn_args = json.loads(fn_args_r) if isinstance(fn_args_r, str) else fn_args_r

            if fn_name == "read_file":
                result = read_file_content(work_dir, fn_args.get("path", f"{entry_file}.py"))
            elif fn_name == "write_file":
                result = write_file_content(work_dir, fn_args.get("path", f"{entry_file}.py"), fn_args.get("content", ""))
            elif fn_name == "run_tests":
                result = run_pytest(work_dir)
            elif fn_name == "finish":
                passed = grade_task(work_dir)
                messages.append({"role": "user", "content": "[Tool: finish]"})
                entry["tool_calls"] = [{"name": "finish", "args": {}, "result": "FINISHED"}]
                turn_log.append(entry)
                return {"passed": passed, "turns_used": turn, "messages": messages, "log": turn_log,
                        "code": read_file_content(work_dir, f"{entry_file}.py")}
            else:
                result = f"Unknown tool: {fn_name}"

            messages.append({"role": "user", "content": f"[Tool: {fn_name}]\n{result[:3000]}"})
            entry.setdefault("tool_calls", []).append({"name": fn_name, "args": fn_args, "result": result[:500]})

        turn_log.append(entry)

    passed = grade_task(work_dir)
    return {"passed": passed, "turns_used": max_turns, "messages": messages, "log": turn_log,
            "code": read_file_content(work_dir, f"{entry_file}.py")}


# ---------------------------------------------------------------------------
# Conditions
# ---------------------------------------------------------------------------

def run_condition(cond, prob, work_dir, seed):
    spec = prob["prompt"]
    enf = prob["name"]
    setup_workspace(prob, work_dir)

    if cond == "continuous":
        r = run_agent(prob, f"## Task\n\n{spec}\n\nWrite your solution to {enf}.py.", TURNS_ALL, work_dir, seed)
        return {"task_id": f"handoff/{prob['name']}", "condition": "continuous", "passed": r["passed"],
                "a_turns": r["turns_used"], "b_turns": 0, "handoff_tokens": 0, "handoff": "", "seed": seed,
                "a_code": r["code"], "b_code": r["code"], "a_log": r["log"], "b_log": []}

    # Agent A
    a = run_agent(prob, f"## Task\n\n{spec}\n\nWrite your solution to {enf}.py.", TURNS_A, work_dir / "a", seed)
    a_code = a["code"]
    test_results = run_pytest(work_dir / "a")

    # Build handoff — FULL transcript from messages, not log
    if cond == "raw":
        parts = []
        for msg in a["messages"]:
            role = msg["role"]
            content = str(msg.get("content", ""))
            # If it's a tool call JSON, try to parse; if truncated, show raw
            if content.startswith('{"__tool_calls__"'):
                try:
                    tc_data = json.loads(content)
                    for tc in tc_data.get("__tool_calls__", []):
                        fn = tc.get("function", {})
                        parts.append(f"[Assistant tool call: {fn.get('name', '?')} args={fn.get('arguments', '{}')}]")
                except json.JSONDecodeError:
                    parts.append(f"[Assistant (truncated tool call)]\n{content[:500]}...")
            else:
                parts.append(f"[{role}]\n{content[:3000]}")
        handoff = "\n".join(parts)
        handoff_tokens = count_completion_tokens(handoff)
        raw_truncation_chars = 3000  # per-message truncation in RAW handoff

    elif cond == "brief":
        prompt = BRIEF_PROMPT.format(entry_file=enf, code=a_code, test_results=test_results)
        brief_text, _ = generate(MODEL, prompt, system="You are helpful.", temperature=0.3, max_tokens=400, seed=seed)
        handoff = brief_text
        # Enforce 400-token cap
        if count_completion_tokens(handoff) > 400:
            handoff = handoff[:1600]  # ~400 tokens
        handoff_tokens = count_completion_tokens(handoff)

    elif cond == "wake":
        prompt = WAKE_PROMPT.format(entry_file=enf, code=a_code, test_results=test_results)
        wake_text, _ = generate(MODEL, prompt, system="You are helpful.", temperature=0.3, max_tokens=500, seed=seed)
        handoff = wake_text
        if count_completion_tokens(handoff) > 500:
            handoff = handoff[:2000]
        handoff_tokens = count_completion_tokens(handoff)

    elif cond == "no_handoff":
        handoff = ""
        handoff_tokens = 0

    # Log A's file state at interrupt point
    a_file_state = {}
    for f in (work_dir / "a").iterdir():
        if f.is_file() and f.suffix == ".py":
            a_file_state[f.name] = f.read_text()

    # Copy A's file state to B's workspace
    b_dir = work_dir / "b"
    b_dir.mkdir(parents=True, exist_ok=True)
    for f in (work_dir / "a").iterdir():
        if f.is_file() and f.suffix == ".py":
            (b_dir / f.name).write_text(f.read_text())

    # Agent B
    b_context_parts = [f"## Task\n\n{spec}"]
    if handoff:
        b_context_parts.append(f"\n## Handoff from previous agent\n\n{handoff}")
    b_context_parts.append(f"\n## Current file state\n\nCode in {enf}.py:\n```\n{a_code}\n```")
    b_context_parts.append(f"\nContinue from where the previous agent left off. Write a correct solution to {enf}.py.")
    b_context = "\n".join(b_context_parts)

    b = run_agent(prob, b_context, TURNS_B, b_dir, seed)
    b_code = b["code"]
    passed = b["passed"] if cond != "no_handoff" else (a["passed"] or b["passed"])

    result = {"task_id": f"handoff/{prob['name']}", "condition": cond, "passed": passed,
              "a_turns": a["turns_used"], "b_turns": b["turns_used"],
              "handoff_tokens": handoff_tokens, "handoff": handoff, "seed": seed,
              "a_code": a_code, "b_code": b_code, "a_log": a["log"], "b_log": b["log"],
              "a_file_state": a_file_state}
    if cond == "raw":
        result["raw_truncation_chars"] = raw_truncation_chars
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    base = Path(__file__).resolve().parent
    data_dir = base / "data_v2"
    data_dir.mkdir(parents=True, exist_ok=True)

    all_results = []
    conditions = ["continuous", "raw", "brief", "wake", "no_handoff"]
    total = len(HARD_PROBLEMS) * len(conditions) * len(SEEDS)
    done = 0

    for seed in SEEDS:
        for prob in HARD_PROBLEMS:
            for cond in conditions:
                work_dir = data_dir / f"{prob['name']}_{cond}_s{seed}"
                done += 1
                print(f"\n[{done}/{total}] {prob['name']:20s} {cond:15s} seed={seed}")
                try:
                    r = run_condition(cond, prob, work_dir, seed)
                    all_results.append(r)
                    print(f"  {'PASS' if r['passed'] else 'FAIL'} | A:{r['a_turns']} B:{r['b_turns']} hoff:{r['handoff_tokens']}")
                except Exception as e:
                    print(f"  ERROR: {e}")
                    import traceback; traceback.print_exc()

    # Save
    # Save compact results (no logs/code)
    out = data_dir / "results.json"
    compact = [{k: v for k, v in r.items() if k not in ("a_log", "b_log", "a_code", "b_code", "messages")} for r in all_results]
    out.write_text(json.dumps(compact, indent=2))
    print(f"\n\nSaved compact results to {out}")

    # Save detailed per-run data including handoff text and code
    for r in all_results:
        run_file = data_dir / f"{r['task_id'].split('/')[1]}_{r['condition']}_s{r['seed']}.json"
        run_file.write_text(json.dumps(r, indent=2, default=str))

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    by_cond = defaultdict(list)
    for r in all_results:
        by_cond[r["condition"]].append(r["passed"])
    for c in conditions:
        p = by_cond[c]
        print(f"  {c:15s}: {sum(p)}/{len(p)} ({100*sum(p)//len(p)}%)")
    print(f"  Total: {len(all_results)} runs")


def run_single_cli():
    """CLI entry point: run a single condition as a subprocess.
    Usage: python3 handoff_v2.py run_single <cond> <prob_name> <seed>
    """
    import sys
    if len(sys.argv) != 5 or sys.argv[1] != "run_single":
        print("Usage: python3 handoff_v2.py run_single <cond> <prob_name> <seed>", file=sys.stderr)
        sys.exit(1)
    cond = sys.argv[2]
    prob_name = sys.argv[3]
    seed = int(sys.argv[4])

    prob = [p for p in HARD_PROBLEMS if p["name"] == prob_name][0]
    data_dir = Path(__file__).resolve().parent / "data_v2"
    work_dir = data_dir / f"{prob_name}_{cond}_s{seed}"

    # Clean work dir if partial previous attempt exists
    if work_dir.exists():
        import shutil
        shutil.rmtree(work_dir)

    r = run_condition(cond, prob, work_dir, seed)
    # Print compact result as JSON for parent to parse
    compact = {k: r[k] for k in ("task_id", "condition", "passed", "a_turns", "b_turns", "handoff_tokens", "seed")}
    if r.get("raw_truncation_chars"):
        compact["raw_truncation_chars"] = r["raw_truncation_chars"]
    print("RESULT:" + json.dumps(compact))

    # Save detailed run data
    run_file = work_dir.parent / f"{prob_name}_{cond}_s{seed}.json"
    run_file.write_text(json.dumps(r, indent=2, default=str))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run_single":
        run_single_cli()
    else:
        main()
