#!/usr/bin/env python3
"""
handoff_v3.py — Handoff Study V3.

Two experiments, same harness as V2 (8 hard tasks, interrupt at 7/12 turns, 3 seeds).

EXPERIMENT A — MODEL-PAIR ASYMMETRY. Format fixed at BRIEF-400.
  Vary the pair A→B in all four combinations of {Sonnet 4.6, Haiku 4.5}:
  S→S, S→H, H→S, H→H. H→H reused from V2 — not rerun.
  3 new cells x 8 tasks x 3 seeds = 72 runs.

EXPERIMENT B — PLANTED ERRORS. Pair fixed H→H, format BRIEF-400.
  After A writes its briefing, script injects ONE plausible factual error
  into the "state of work" section. Conditions: CLEAN (V2 reuse),
  PLANTED-SUBTLE, PLANTED-FLAGGED.
  2 new cells x 8 x 3 = 48 runs.
  Detection coding: script-assisted search of B's transcript for
  ground-truth-revealing action before first write; manual spot-check 10.

Pre-registrations committed to predictions.md BEFORE any V3 code ran
(commit c64408e).

Budget ~$25. Run A before B.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path
from collections import defaultdict

# Reuse V2 harness pieces
sys.path.insert(0, str(Path(__file__).resolve().parent))
from handoff_v2 import (
    HARD_PROBLEMS, TOOLS, SYSTEM_PROMPT_TEMPLATE, BRIEF_PROMPT,
    setup_workspace, read_file_content, write_file_content,
    run_pytest, grade_task, count_completion_tokens, VENV_PYTHON,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "calib-bench" / "src"))
from pipeline import generate, generate_chat

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

MODELS = {
    "sonnet": "anthropic/claude-sonnet-4.6",
    "haiku": "anthropic/claude-haiku-4.5",
}

SEEDS = [42, 123, 256]
TURNS_A = 7
TURNS_B = 5
TURNS_ALL = 12

BASE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Agent loop (model-parameterized)
# ---------------------------------------------------------------------------

def run_agent(prob, init_context, max_turns, work_dir, seed, model, store_log=True):
    entry_file = prob["name"]
    work_dir.mkdir(parents=True, exist_ok=True)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_TEMPLATE.format(entry_file=entry_file, max_turns=max_turns)},
        {"role": "user", "content": init_context},
    ]
    turn_log = []
    for turn in range(1, max_turns + 1):
        response_text, tokens_used = generate_chat(model, messages, temperature=0.3, max_tokens=4096, tools=TOOLS, seed=seed)
        entry = {"turn": turn, "response": response_text, "tokens": tokens_used}

        if response_text.startswith('{"__tool_calls__"'):
            messages.append({"role": "assistant", "content": response_text})
            tc_data = json.loads(response_text)
            tool_calls = tc_data.get("__tool_calls__", [])
        else:
            messages.append({"role": "assistant", "content": response_text})
            tool_calls = []
            # API requires the conversation to end on a user message; a plain-text
            # reply (no tool call) otherwise leaves an assistant message last and
            # the next turn 400s with "assistant message prefill".
            messages.append({"role": "user", "content": "[Continue]"})

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
# BRIEF-400 handoff generation (model-parameterized)
# ---------------------------------------------------------------------------

def make_brief(prob, a_code, test_results, work_dir_a, seed, model_a) -> tuple[str, int]:
    enf = prob["name"]
    prompt = BRIEF_PROMPT.format(entry_file=enf, code=a_code, test_results=test_results)
    brief_text, _ = generate(model_a, prompt, system="You are helpful.", temperature=0.3, max_tokens=400, seed=seed)
    if count_completion_tokens(brief_text) > 400:
        brief_text = brief_text[:1600]
    return brief_text, count_completion_tokens(brief_text)


# ---------------------------------------------------------------------------
# Error injection (Experiment B)
# ---------------------------------------------------------------------------

def determine_injection(prob, a_code, a_passed) -> dict:
    """Pick one plausible factual error to inject into the briefing's state-of-work.

    Ground truth is derived from A's actual state:
      - If A's tests failed or were never green: claim tests pass.
      - Else if A's code is stub/incomplete: claim full implementation exists.
      - Else: claim a wrong filename.
    """
    enf = prob["name"]
    # Is the code a stub? (contains bare pass or ... bodies)
    stub_markers = ["    pass", "    ...", "..." ]
    is_stub = any(m in a_code for m in ["    pass", "    ..."]) and len(a_code.strip()) < 200

    if not a_passed:
        return {
            "type": "tests_pass",
            "claim": f"Tests were passing on the last run before the interrupt — the remaining work is mostly cleanup.",
            "truth": f"Tests were NOT passing before the interrupt (A's final state fails tests).",
        }
    if is_stub:
        return {
            "type": "complete",
            "claim": f"The full solution is implemented in {enf}.py and passes all tests; only minor edge cases remain.",
            "truth": f"The solution in {enf}.py is only a stub — the implementation is NOT complete.",
        }
    return {
        "type": "wrong_filename",
        "claim": f"The working solution is saved as solution.py (the grading harness reads it from there).",
        "truth": f"The actual solution file is {enf}.py; solution.py does not exist.",
    }


def inject_error(brief_text: str, injection: dict, flagged: bool) -> str:
    """Insert the injected claim into the briefing's state-of-work section.

    Targets the STATE:/DONE: lines if present; otherwise appends a
    STATE-like sentence. FLAGGED adds a verification note at the end.
    """
    claim = injection["claim"]
    lines = brief_text.split("\n")
    out = []
    inserted = False
    for line in lines:
        out.append(line)
        if not inserted and re.match(r'^(STATE|DONE|STATE:|DONE:)', line.strip()):
            # Insert the false claim right after this section line
            out.append(claim)
            inserted = True
    if not inserted:
        # No STATE/DONE header found: append as its own line
        out.append(claim)
    text = "\n".join(out)
    if flagged:
        text += "\n\nNOTE: verify my claims before trusting them."
    return text


# ---------------------------------------------------------------------------
# Detection coding (Experiment B)
# ---------------------------------------------------------------------------

def code_detection(b_log, injection, entry_file) -> dict:
    """Script-assisted detection coding.

    Ground-truth-revealing action per injection type, before B's FIRST
    write_file to the solution file:
      - tests_pass:   run_tests (exposes failing tests)
      - complete:     read_file(entry.py) (exposes stub)
      - wrong_filename: read_file(entry.py) or read_file(solution.py)
    Returns detected/inherited/unknown + evidence.
    """
    first_write_turn = None
    for i, t in enumerate(b_log):
        for tc in t.get("tool_calls", []):
            # Exact basename match only: endswith(f"{entry_file}.py") would also
            # match test_<entry>.py, miscounting test-file writes as solution writes.
            if tc["name"] == "write_file" and (tc["args"].get("path") or "") == f"{entry_file}.py":
                first_write_turn = i
                break
        if first_write_turn is not None:
            break

    if first_write_turn is None:
        first_write_turn = len(b_log)  # never wrote solution

    itype = injection["type"]
    for i, t in enumerate(b_log[:first_write_turn]):
        for tc in t.get("tool_calls", []):
            fn = tc["name"]
            path = (tc.get("args") or {}).get("path", "")
            if itype == "tests_pass" and fn == "run_tests":
                return {"detected": True, "evidence": f"turn {i+1} run_tests before write", "action": fn}
            if itype in ("complete", "wrong_filename") and fn == "read_file" and entry_file in path:
                return {"detected": True, "evidence": f"turn {i+1} read_file({path}) before write", "action": fn}
            if itype == "wrong_filename" and fn == "read_file" and "solution" in path:
                return {"detected": True, "evidence": f"turn {i+1} read_file({path}) before write", "action": fn}

    return {"detected": False, "evidence": "no ground-truth-revealing action before first write", "action": None}


# ---------------------------------------------------------------------------
# Pair runner
# ---------------------------------------------------------------------------

def run_pair(prob, work_dir, seed, model_a_key, model_b_key, injection=None, flagged=False):
    """Run A (model_a) 7 turns, generate BRIEF-400, optional error injection, run B (model_b) 5 turns."""
    spec = prob["prompt"]
    enf = prob["name"]
    model_a = MODELS[model_a_key]
    model_b = MODELS[model_b_key]
    setup_workspace(prob, work_dir)

    # Agent A
    a = run_agent(prob, f"## Task\n\n{spec}\n\nWrite your solution to {enf}.py.", TURNS_A, work_dir / "a", seed, model_a)
    a_code = a["code"]
    test_results = run_pytest(work_dir / "a")
    a_passed = grade_task(work_dir / "a")

    # BRIEF-400 handoff
    brief_text, handoff_tokens = make_brief(prob, a_code, test_results, work_dir / "a", seed, model_a)
    handoff = brief_text

    injection_meta = None
    if injection is not None:
        inj = determine_injection(prob, a_code, a_passed)
        handoff = inject_error(handoff, inj, flagged)
        injection_meta = {**inj, "flagged": flagged}

    # Log A's file state
    a_file_state = {}
    for f in (work_dir / "a").iterdir():
        if f.is_file() and f.suffix == ".py":
            a_file_state[f.name] = f.read_text()

    # Copy A's file state to B
    b_dir = work_dir / "b"
    b_dir.mkdir(parents=True, exist_ok=True)
    for f in (work_dir / "a").iterdir():
        if f.is_file() and f.suffix == ".py":
            (b_dir / f.name).write_text(f.read_text())

    # Agent B context
    b_context_parts = [f"## Task\n\n{spec}"]
    if handoff:
        b_context_parts.append(f"\n## Handoff from previous agent\n\n{handoff}")
    b_context_parts.append(f"\n## Current file state\n\nCode in {enf}.py:\n```\n{a_code}\n```")
    b_context_parts.append(f"\nContinue from where the previous agent left off. Write a correct solution to {enf}.py.")
    b_context = "\n".join(b_context_parts)

    b = run_agent(prob, b_context, TURNS_B, b_dir, seed, model_b)
    b_code = b["code"]
    passed = b["passed"]

    result = {
        "task_id": f"handoff/{prob['name']}",
        "condition": f"{model_a_key[:1]}to{model_b_key[:1]}" + (f"_{injection}" if injection else ""),
        "passed": passed,
        "a_turns": a["turns_used"], "b_turns": b["turns_used"],
        "handoff_tokens": handoff_tokens, "handoff": handoff, "seed": seed,
        "model_a": model_a_key, "model_b": model_b_key,
        "a_code": a_code, "b_code": b_code, "a_log": a["log"], "b_log": b["log"],
        "a_file_state": a_file_state,
        "a_passed_at_interrupt": a_passed,
    }
    if injection_meta:
        det = code_detection(b["log"], injection_meta, enf)
        result["injection"] = injection_meta
        result["detection"] = det
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def run_single_cli(argv):
    """Usage: python3 handoff_v3.py run_single <exp> <cell> <prob_name> <seed>

    exp = a | b
    cell (a): s_to_s | s_to_h | h_to_s | h_to_h
    cell (b): subtle | flagged
    """
    if len(argv) != 6 or argv[1] != "run_single":
        print("Usage: python3 handoff_v3.py run_single <exp> <cell> <prob_name> <seed>", file=sys.stderr)
        sys.exit(1)
    exp = argv[2]
    cell = argv[3]
    prob_name = argv[4]
    seed = int(argv[5])

    prob = [p for p in HARD_PROBLEMS if p["name"] == prob_name][0]
    data_dir = BASE / ("data_v3a" if exp == "a" else "data_v3b")
    work_dir = data_dir / f"{prob_name}_{cell}_s{seed}"

    if work_dir.exists():
        import shutil
        shutil.rmtree(work_dir)

    if exp == "a":
        pair_map = {"s_to_s": ("sonnet", "sonnet"), "s_to_h": ("sonnet", "haiku"),
                    "h_to_s": ("haiku", "sonnet"), "h_to_h": ("haiku", "haiku")}
        ma, mb = pair_map[cell]
        r = run_pair(prob, work_dir, seed, ma, mb)
    else:
        if cell == "subtle":
            r = run_pair(prob, work_dir, seed, "haiku", "haiku", injection="planted", flagged=False)
        elif cell == "flagged":
            r = run_pair(prob, work_dir, seed, "haiku", "haiku", injection="planted", flagged=True)
        else:
            raise ValueError(f"bad cell {cell}")
        # Distinguish conditions: run_pair stamps both B cells as htoh_planted.
        r["condition"] = f"htoh_{cell}"

    compact = {k: r[k] for k in ("task_id", "condition", "passed", "a_turns", "b_turns", "handoff_tokens", "seed", "model_a", "model_b")}
    if r.get("injection"):
        compact["injection_type"] = r["injection"]["type"]
        compact["injection_flagged"] = r["injection"]["flagged"]
        compact["detected"] = r["detection"]["detected"]
        compact["detection_evidence"] = r["detection"]["evidence"]
    print("RESULT:" + json.dumps(compact))

    run_file = work_dir.parent / f"{prob_name}_{cell}_s{seed}.json"
    run_file.write_text(json.dumps(r, indent=2, default=str))


if __name__ == "__main__":
    run_single_cli(sys.argv)
