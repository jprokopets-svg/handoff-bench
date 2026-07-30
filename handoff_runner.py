#!/usr/bin/env python3
"""
handoff_runner.py — Handoff Study Pilot.

Question: when an agent must stop mid-task and brief a successor,
what briefing format best preserves task success?

Conditions:
  RAW       — A's full transcript passed verbatim to B
  BRIEF     — A writes a structured briefing (max 400 tokens)
  NO-HANDOFF — B gets task spec + file state only (control)
  CONTINUOUS — one agent, 10 uninterrupted turns (ceiling)

24 runs (6 tasks x 4 conditions x 1 seed). Budget ~$3.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "calib-bench" / "src"))
from pipeline import generate, generate_chat, is_openrouter_model

# ---------------------------------------------------------------------------
# Problems (6 MBPP-hard / code-hard style, from calib-bench agentic_mid pool)
# ---------------------------------------------------------------------------

PROBLEMS = [
    {
        "name": "longest_prefix",
        "prompt": "Write a function to find the longest common prefix string among an array of strings. Return empty string if none.",
        "func_sig": "def longest_common_prefix(strs: list[str]) -> str:",
        "tests": [
            "assert longest_common_prefix(['flower','flow','flight']) == 'fl'",
            "assert longest_common_prefix(['dog','racecar','car']) == ''",
            "assert longest_common_prefix(['']) == ''",
            "assert longest_common_prefix(['a']) == 'a'",
            "assert longest_common_prefix(['abc','abc','abc']) == 'abc'",
            "assert longest_common_prefix(['interspecies','interstellar','interstate']) == 'inters'",
        ],
    },
    {
        "name": "parentheses",
        "prompt": "Write a function that generates all valid combinations of n pairs of parentheses.",
        "func_sig": "def generate_parentheses(n: int) -> list[str]:",
        "tests": [
            "assert sorted(generate_parentheses(1)) == sorted(['()'])",
            "assert sorted(generate_parentheses(2)) == sorted(['()()', '(())'])",
            "assert len(generate_parentheses(3)) == 5",
            "assert sorted(generate_parentheses(3)) == sorted(['((()))','(()())','(())()','()(())','()()()'])",
        ],
    },
    {
        "name": "power_set",
        "prompt": "Write a function that returns the power set of a given set of distinct integers.",
        "func_sig": "def power_set(nums: list[int]) -> list[list[int]]:",
        "tests": [
            "assert sorted(power_set([1])) == sorted([[], [1]])",
            "assert sorted(power_set([1,2])) == sorted([[], [1], [2], [1,2]])",
            "assert len(power_set([1,2,3])) == 8",
        ],
    },
    {
        "name": "palindromic_substring",
        "prompt": "Write a function that returns the longest palindromic substring in a given string.",
        "func_sig": "def longest_palindrome(s: str) -> str:",
        "tests": [
            "assert longest_palindrome('babad') in ('bab', 'aba')",
            "assert longest_palindrome('cbbd') == 'bb'",
            "assert longest_palindrome('a') == 'a'",
            "assert longest_palindrome('ac') in ('a', 'c')",
        ],
    },
    {
        "name": "three_sum",
        "prompt": "Write a function that finds all unique triplets in an array that sum to zero.",
        "func_sig": "def three_sum(nums: list[int]) -> list[list[int]]:",
        "tests": [
            "assert three_sum([-1,0,1,2,-1,-4]) == [[-1,-1,2],[-1,0,1]]",
            "assert three_sum([0,1,1]) == []",
            "assert three_sum([0,0,0]) == [[0,0,0]]",
        ],
    },
    {
        "name": "rain_water",
        "prompt": "Write a function that calculates how much water can be trapped after raining, given an array of non-negative integers representing elevation heights.",
        "func_sig": "def trap(height: list[int]) -> int:",
        "tests": [
            "assert trap([0,1,0,2,1,0,1,3,2,1,2,1]) == 6",
            "assert trap([4,2,0,3,2,5]) == 9",
            "assert trap([1,0,1]) == 1",
        ],
    },
]

MODEL = "anthropic/claude-haiku-4.5"
SEED = 42
MAX_TURNS_A = 4
MAX_TURNS_B = 6
MAX_TURNS_CONTINUOUS = 10

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

Your goal: write a correct solution function that passes all provided tests.

Your task: Write a correct solution function in {entry_file}.py. The test file is test_{entry_file}.py.

CRITICAL: You MUST write code. Reading files alone does nothing. Follow this protocol exactly:

1. Read the test file ONCE to understand what's expected.
2. IMMEDIATELY write a solution to {entry_file}.py using write_file.
3. Run tests with run_tests().
4. If tests fail, fix your code with write_file and test again.
5. Call finish() when all tests pass.

IMPORTANT: Do not read files more than once. Writing and testing is how you make progress."""

BRIEFING_PROMPT = """You are being interrupted mid-task. Write a BRIEFING for the next agent who will continue your work.

Maximum 400 tokens. Format as:

GOAL: <what the task requires>
STATE: <what exists so far, including any written code>
DONE: <what is working / resolved>
BROKEN: <what is broken, failing, or unknown>
NEXT: <the single most important thing to try next>

Current code in {entry_file}.py:
```
{code}
```

Test results so far:
{test_results}

Write your briefing:"""


# ---------------------------------------------------------------------------
# Workspace helpers
# ---------------------------------------------------------------------------

def setup_workspace(prob: dict, work_dir: Path):
    """Create a fresh workspace for a task."""
    work_dir.mkdir(parents=True, exist_ok=True)
    entry_file = work_dir / f"{prob['name']}.py"
    if entry_file.exists():
        entry_file.unlink()
    # Write a stub
    entry_file.write_text(
        f"{prob['func_sig']}\n    # TODO: implement\n    pass\n"
    )
    # Write tests file
    test_path = work_dir / f"test_{prob['name']}.py"
    test_code = "\n".join([
        f"from {prob['name']} import *",
        "",
        "import pytest",
        "",
        *[f"\n{t}" for t in prob["tests"]],
    ])
    test_path.write_text(test_code)
    return entry_file


def read_file_content(work_dir: Path, filename: str) -> str:
    """Read a file from the workspace, return content or error."""
    if not filename or filename.strip() in ("/", "."):
        return f"ERROR: invalid path '{filename}'"
    path = work_dir / filename
    if path.exists() and path.is_file():
        return path.read_text()
    if path.exists() and path.is_dir():
        return f"ERROR: '{filename}' is a directory, not a file"
    return f"ERROR: file {filename} not found"


def write_file_content(work_dir: Path, filename: str, content: str):
    """Write content to a file in the workspace."""
    path = work_dir / filename
    path.write_text(content)
    return f"Written to {filename}"


VENV_PYTHON = str(Path(__file__).resolve().parent / ".venv" / "bin" / "python3")


def run_pytest(work_dir: Path) -> str:
    """Run pytest and return results."""
    python = VENV_PYTHON if Path(VENV_PYTHON).exists() else "python3"
    result = subprocess.run(
        [python, "-m", "pytest", str(work_dir), "-v", "--tb=short", "-q"],
        capture_output=True, text=True, timeout=30
    )
    output = result.stdout + result.stderr
    return output[-2000:] if len(output) > 2000 else output


def grade_task(work_dir: Path) -> bool:
    """Return True if all tests pass."""
    python = VENV_PYTHON if Path(VENV_PYTHON).exists() else "python3"
    result = subprocess.run(
        [python, "-m", "pytest", str(work_dir), "-q", "--tb=no"],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

def run_agent(
    prob: dict,
    initial_context: str,
    max_turns: int,
    work_dir: Path,
    store: dict | None = None,
) -> dict:
    """Run the agent loop for a given number of turns."""
    entry_file = prob["name"]
    work_dir.mkdir(parents=True, exist_ok=True)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_TEMPLATE.format(
            entry_file=entry_file, max_turns=max_turns)},
        {"role": "user", "content": initial_context},
    ]

    turn_log = []
    passed = False

    for turn in range(1, max_turns + 1):
        response_text, tokens_used = generate_chat(
            MODEL, messages,
            temperature=0.3, max_tokens=4096,
            tools=TOOLS, seed=SEED,
        )

        # Handle tool calls
        if response_text.startswith('{"__tool_calls__"'):
            tc_data = json.loads(response_text)
            tool_calls = tc_data.get("__tool_calls__", [])
        else:
            tool_calls = []

        turn_entry = {"turn": turn, "response": response_text, "tokens": tokens_used}

        if not tool_calls:
            # No tool calls — just assistant text. Add to messages and continue.
            messages.append({"role": "assistant", "content": response_text})
            turn_log.append(turn_entry)
            continue

        # Add the assistant's response (with function calls) to message history
        if response_text.startswith('{"__tool_calls__"'):
            messages.append({"role": "assistant", "content": response_text})
        else:
            messages.append({"role": "assistant", "content": response_text})

        # Process tool calls
        for tc in tool_calls:
            fn_name = tc.get("function", {}).get("name", "")
            fn_args_raw = tc.get("function", {}).get("arguments", "{}")
            try:
                if isinstance(fn_args_raw, str):
                    fn_args = json.loads(fn_args_raw)
                else:
                    fn_args = fn_args_raw
            except (json.JSONDecodeError, TypeError):
                fn_args = {}

            if fn_name == "read_file":
                path = fn_args.get("path", entry_file + ".py")
                result = read_file_content(work_dir, path)
            elif fn_name == "write_file":
                path = fn_args.get("path", entry_file + ".py")
                content = fn_args.get("content", "")
                result = write_file_content(work_dir, path, content)
            elif fn_name == "run_tests":
                result = run_pytest(work_dir)
            elif fn_name == "finish":
                result = "FINISHED"
                passed = grade_task(work_dir)
            else:
                result = f"Unknown tool: {fn_name}"

            # Add tool response to messages
            tool_msg = {
                "role": "user",
                "content": f"[Tool: {fn_name}]\n{result[:3000]}"
            }
            messages.append(tool_msg)
            turn_entry.setdefault("tool_calls", []).append({
                "name": fn_name, "args": fn_args, "result": result[:500]
            })

            if fn_name == "finish":
                turn_log.append(turn_entry)
                return {
                    "passed": passed,
                    "turns_used": turn,
                    "messages": messages,
                    "log": turn_log,
                    "code": read_file_content(work_dir, entry_file + ".py"),
                }

        turn_log.append(turn_entry)

    # Timeout — grade current state
    passed = grade_task(work_dir)
    return {
        "passed": passed,
        "turns_used": max_turns,
        "messages": messages,
        "log": turn_log,
        "code": read_file_content(work_dir, entry_file + ".py"),
    }


# ---------------------------------------------------------------------------
# Conditions
# ---------------------------------------------------------------------------

def run_raw(prob: dict, work_dir: Path) -> dict:
    """RAW: A's full transcript passed verbatim to B."""
    spec = prob["prompt"]
    entry_file = prob["name"]

    # Agent A
    setup_workspace(prob, work_dir)
    a_result = run_agent(prob, f"## Task\n\n{spec}\n\nWrite your solution to {entry_file}.py.", MAX_TURNS_A, work_dir)

    # Build RAW handoff = full transcript
    transcript_parts = []
    for entry in a_result["log"]:
        transcript_parts.append(f"--- Turn {entry['turn']} ---\n{entry['response']}")
        for tc in entry.get("tool_calls", []):
            transcript_parts.append(f"[Tool: {tc['name']}]\n{tc['result']}")
    handoff = "\n".join(transcript_parts)
    handoff_tokens = len(handoff.split())

    # Agent B
    b_context = (
        f"## Task\n\n{spec}\n\n"
        f"## Previous agent's work\n\n"
        f"The following is the full transcript of a previous agent's attempt:\n\n"
        f"{handoff}\n\n"
        f"## Current state\n\n"
        f"Code in {entry_file}.py:\n```\n{a_result['code']}\n```\n\n"
        f"Continue from where they left off. Write a correct solution to {entry_file}.py."
    )
    b_result = run_agent(prob, b_context, MAX_TURNS_B, work_dir)

    return {
        "task_id": f"handoff/{prob['name']}",
        "condition": "raw",
        "passed": b_result["passed"],
        "a_turns": a_result["turns_used"],
        "b_turns": b_result["turns_used"],
        "handoff_tokens": handoff_tokens,
        "seed": SEED,
        "a_log": a_result["log"],
        "b_log": b_result["log"],
        "handoff": handoff,
    }


def run_brief(prob: dict, work_dir: Path) -> dict:
    """BRIEF: A writes a structured briefing, max 400 tokens."""
    spec = prob["prompt"]
    entry_file = prob["name"]

    # Agent A
    setup_workspace(prob, work_dir)
    a_result = run_agent(prob, f"## Task\n\n{spec}\n\nWrite your solution to {entry_file}.py.", MAX_TURNS_A, work_dir)

    # A writes briefing
    code = a_result["code"]
    test_results = run_pytest(work_dir)
    brief_prompt = BRIEFING_PROMPT.format(entry_file=entry_file, code=code, test_results=test_results)
    brief_text, brief_tokens = generate(MODEL, brief_prompt, system="You are a helpful assistant.", temperature=0.3, max_tokens=400, seed=SEED)
    handoff_tokens = brief_tokens

    # Agent B
    b_context = (
        f"## Task\n\n{spec}\n\n"
        f"## Briefing from previous agent\n\n"
        f"{brief_text}\n\n"
        f"## Current state\n\n"
        f"Code in {entry_file}.py:\n```\n{code}\n```\n\n"
        f"Continue from where the previous agent left off. Write a correct solution to {entry_file}.py."
    )
    b_result = run_agent(prob, b_context, MAX_TURNS_B, work_dir)

    return {
        "task_id": f"handoff/{prob['name']}",
        "condition": "brief",
        "passed": b_result["passed"],
        "a_turns": a_result["turns_used"],
        "b_turns": b_result["turns_used"],
        "handoff_tokens": handoff_tokens,
        "seed": SEED,
        "a_log": a_result["log"],
        "b_log": b_result["log"],
        "handoff": brief_text,
    }


def run_no_handoff(prob: dict, work_dir: Path) -> dict:
    """NO-HANDOFF: B gets task spec + file state only."""
    spec = prob["prompt"]
    entry_file = prob["name"]

    # No Agent A — just set up workspace
    setup_workspace(prob, work_dir)
    code = read_file_content(work_dir, entry_file + ".py")

    b_context = (
        f"## Task\n\n{spec}\n\n"
        f"## Starter code\n\n"
        f"Code in {entry_file}.py:\n```\n{code}\n```\n\n"
        f"Write a correct solution to {entry_file}.py. You have no previous agent's work to reference."
    )
    b_result = run_agent(prob, b_context, MAX_TURNS_B, work_dir)

    return {
        "task_id": f"handoff/{prob['name']}",
        "condition": "no_handoff",
        "passed": b_result["passed"],
        "a_turns": 0,
        "b_turns": b_result["turns_used"],
        "handoff_tokens": 0,
        "seed": SEED,
        "a_log": [],
        "b_log": b_result["log"],
        "handoff": "",
    }


def run_continuous(prob: dict, work_dir: Path) -> dict:
    """CONTINUOUS: one agent, 10 uninterrupted turns (ceiling)."""
    spec = prob["prompt"]
    entry_file = prob["name"]

    setup_workspace(prob, work_dir)
    result = run_agent(prob, f"## Task\n\n{spec}\n\nWrite your solution to {entry_file}.py.", MAX_TURNS_CONTINUOUS, work_dir)

    return {
        "task_id": f"handoff/{prob['name']}",
        "condition": "continuous",
        "passed": result["passed"],
        "a_turns": result["turns_used"],
        "b_turns": 0,
        "handoff_tokens": 0,
        "seed": SEED,
        "a_log": result["log"],
        "b_log": [],
        "handoff": "",
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Run all 24 evaluations."""
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    results = []
    runners = {
        "raw": run_raw,
        "brief": run_brief,
        "no_handoff": run_no_handoff,
        "continuous": run_continuous,
    }

    for prob in PROBLEMS:
        for cond_name, runner_fn in runners.items():
            work_dir = data_dir / f"{prob['name']}_{cond_name}"
            print(f"\n{'='*60}")
            print(f"Task: {prob['name']}  Condition: {cond_name}")
            print(f"{'='*60}")

            try:
                result = runner_fn(prob, work_dir)
                results.append(result)
                print(f"  Result: {'PASS' if result['passed'] else 'FAIL'}")
                print(f"  A turns: {result['a_turns']}, B turns: {result['b_turns']}, handoff tokens: {result['handoff_tokens']}")
            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback
                traceback.print_exc()

            # Save per-run log
            log_path = data_dir / f"{prob['name']}_{cond_name}.json"
            log_path.write_text(json.dumps({"task_id": f"handoff/{prob['name']}", "condition": cond_name}) + "\n")

    # Save results
    out_path = data_dir / "results.json"
    results_json = []
    for r in results:
        results_json.append({
            "task_id": r["task_id"],
            "condition": r["condition"],
            "passed": r["passed"],
            "a_turns": r["a_turns"],
            "b_turns": r["b_turns"],
            "handoff_tokens": r["handoff_tokens"],
            "seed": r["seed"],
        })
    out_path.write_text(json.dumps(results_json, indent=2))
    print(f"\n\nResults saved to {out_path}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    by_condition = defaultdict(list)
    for r in results:
        by_condition[r["condition"]].append(r["passed"])

    for cond in ["raw", "brief", "no_handoff", "continuous"]:
        passes = by_condition[cond]
        n = len(passes)
        n_pass = sum(passes)
        print(f"  {cond:15s}: {n_pass}/{n} ({100*n_pass//n}%)")


if __name__ == "__main__":
    main()
