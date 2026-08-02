#!/usr/bin/env python3
"""part3/stage0_harness.py — Handoff Part III Stage 0 cross-family transport test.

Tests transport, not science: for each of the four collective families
(Claude, GPT, Gemini, DeepSeek), run the handoff transport loop end-to-end
on 5 non-study tasks (self-pair A=B=same family), one CLEAN-style BRIEF-400
briefing per run, and verify briefing consumption behaviorally from the
transcript (read_briefing before first solution-file write).

Reuses V2/V3 code by import; no existing files are modified. New code lives
under part3/ only, per Stage 0 authorization (Buzz event 79096ec2) and
STAGE0_PREREG.md.

Usage:  .venv/bin/python3 part3/stage0_harness.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent          # part3/
REPO = BASE.parent                               # handoff-bench/
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(REPO.parent / "calib-bench" / "src"))

from handoff_v2 import (  # noqa: E402  (reuse by import)
    setup_workspace, read_file_content, write_file_content,
    count_completion_tokens, VENV_PYTHON,
    SYSTEM_PROMPT_TEMPLATE, BRIEF_PROMPT,
)
from stage0_tasks import STAGE0_TASKS  # noqa: E402

# ---------------------------------------------------------------------------
# Configuration (Stage 0 prereg: section a)
# ---------------------------------------------------------------------------

FAMILIES = {
    "claude":   "anthropic/claude-haiku-4.5",
    "gpt":      "openai/gpt-5-mini",
    "gemini":   "google/gemini-2.5-flash",
    "deepseek": "deepseek/deepseek-v3.2",
}

SEED = 42
TURNS_A = 7
TURNS_B = 5
BUDGET_CAP = 8.0          # hard stop, below the $10 cap (prereg)
MAX_CALL_RETRIES = 2      # retries for API/schema errors only (prereg c)

RUN_DIR = BASE / "run_logs"

TOOLS = [
    {"type": "function", "function": {"name": "read_file", "description": "Read a file from the workspace",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "write_file", "description": "Write content to a file",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "run_tests", "description": "Run pytest on the solution file",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "finish", "description": "Submit the current solution and stop",
        "parameters": {"type": "object", "properties": {}}}},
]

READ_BRIEFING_TOOL = {"type": "function", "function": {"name": "read_briefing",
    "description": "Read the briefing left by the previous agent (briefing.txt in the workspace)",
    "parameters": {"type": "object", "properties": {"path": {"type": "string"}}}}}

B_TOOLS = TOOLS + [READ_BRIEFING_TOOL]

KNOWN_TOOLS = {"read_file", "write_file", "run_tests", "finish", "read_briefing"}

B_SYSTEM_EXTRA = (
    "\n\nA briefing written by the previous agent is stored in briefing.txt. "
    "You MUST call read_briefing to read it BEFORE writing any solution code. "
    "The briefing contains the previous agent's understanding of the task — use it."
)


# ---------------------------------------------------------------------------
# API layer (returns text, tokens, cost; retries API/schema errors only)
# ---------------------------------------------------------------------------

def _load_key() -> str:
    dotenv = REPO.parent / "calib-bench" / ".env"
    if dotenv.exists():
        for line in dotenv.read_text().splitlines():
            line = line.strip()
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = os.environ.get("OPENROUTER_API_KEY") or _load_key()


class APIFailure(Exception):
    """API/schema error — excludable per prereg (c)."""


def api_call(model: str, messages: list[dict], *, temperature: float = 0.3,
             max_tokens: int = 4096, tools: list[dict] | None = None,
             seed: int = SEED) -> tuple[str, int, float]:
    if not KEY:
        raise APIFailure("OPENROUTER_API_KEY not set")
    payload = {"model": model, "messages": messages, "temperature": temperature,
               "max_tokens": max_tokens}
    if tools:
        payload["tools"] = tools
    if seed is not None:
        payload["seed"] = seed
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise APIFailure(f"HTTP {e.code}: {e.read().decode()[:300]}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        raise APIFailure(f"transport: {e}")

    choice = result.get("choices", [{}])[0]
    msg = choice.get("message", {})
    usage = result.get("usage", {})
    tokens = usage.get("total_tokens", 0)
    cost = float(usage.get("cost", 0.0) or 0.0)

    tool_calls = msg.get("tool_calls")
    if tool_calls:
        return json.dumps({"__tool_calls__": tool_calls}), tokens, cost
    text = msg.get("content") or ""
    if not text:
        # Degenerate: no content and no tool calls (e.g., reasoning-only
        # response that consumed the budget) — excludable schema error.
        raise APIFailure(f"degenerate empty response (finish={choice.get('finish_reason')})")
    return text, tokens, cost


def call_with_retry(model: str, messages: list[dict], **kw) -> tuple[str, int, float]:
    last_err = None
    for attempt in range(MAX_CALL_RETRIES + 1):
        try:
            return api_call(model, messages, **kw)
        except APIFailure as e:
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise last_err


# ---------------------------------------------------------------------------
# Deterministic grading (mirrors "deterministic executable task success";
# immune to pytest's no-tests-collected exit code 5 and to agents rewriting
# test files — always execs the ORIGINAL test snapshot)
# ---------------------------------------------------------------------------

def snapshot_tests(work_dir, entry_file) -> None:
    src = work_dir / f"test_{entry_file}.py"
    dst = work_dir / f"test_{entry_file}.py.orig"
    dst.write_text(src.read_text())


def _run_test_exec(python, work_dir, entry_file):
    test_file = work_dir / f"test_{entry_file}.py.orig"
    if not test_file.exists():
        test_file = work_dir / f"test_{entry_file}.py"
    code = (
        "import sys, runpy; "
        f"sys.path.insert(0, {str(work_dir.resolve())!r}); "
        f"runpy.run_path({str(test_file.resolve())!r}, run_name='__main__')"
    )
    try:
        return subprocess.run([python, "-c", code], capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return None


def grade_entry(work_dir, entry_file) -> bool:
    python = VENV_PYTHON if Path(VENV_PYTHON).exists() else "python3"
    r = _run_test_exec(python, work_dir, entry_file)
    return bool(r and r.returncode == 0)


def tests_feedback(work_dir, entry_file) -> str:
    """Run the original test snapshot; return compact PASS/FAIL feedback."""
    python = VENV_PYTHON if Path(VENV_PYTHON).exists() else "python3"
    r = _run_test_exec(python, work_dir, entry_file)
    if r is None:
        return "[Tests] TIMEOUT"
    if r.returncode == 0:
        return "[Tests] All tests passed (PASS)."
    tail = (r.stdout + r.stderr)[-1500:]
    return f"[Tests] FAILED:\n{tail}"


# ---------------------------------------------------------------------------
# Agent loop (model-parameterized, tool-metadata logging, retry on API errors)
# ---------------------------------------------------------------------------

def _parse_args(fn_args_r):
    if isinstance(fn_args_r, dict):
        return fn_args_r, False
    try:
        return json.loads(fn_args_r), False
    except (json.JSONDecodeError, TypeError):
        return {}, True


def run_agent(prob, init_context, max_turns, work_dir, seed, model, role,
              tools=None, system_extra="", tool_protocol="json"):
    """Run one agent. Returns dict with passed/turns/cost/tool_log or
    {'error': 'api_failure: ...'} (excludable).

    tool_protocol: 'json' = V2/V3 JSON-string-in-content convention;
    'openai' = canonical OpenAI assistant-tool_calls + role-tool messages
    (per-family adapter for Gemini, which otherwise imitates the raw JSON
    in its history as truncated plain-text content).
    """
    entry_file = prob["name"]
    work_dir.mkdir(parents=True, exist_ok=True)
    system = SYSTEM_PROMPT_TEMPLATE.format(entry_file=entry_file, max_turns=max_turns) + system_extra
    messages = [{"role": "system", "content": system},
                {"role": "user", "content": init_context}]
    tool_log = []
    cost = 0.0
    toolset = tools or TOOLS

    for turn in range(1, max_turns + 1):
        response_text = None
        for attempt in range(MAX_CALL_RETRIES + 1):
            try:
                response_text, toks, c = call_with_retry(
                    model, messages, temperature=0.3, max_tokens=4096, tools=toolset, seed=seed)
                if response_text.startswith('{"__tool_calls__"'):
                    tc_data = json.loads(response_text)  # may raise JSONDecodeError
                break
            except (APIFailure, json.JSONDecodeError) as e:
                if attempt >= MAX_CALL_RETRIES:
                    return {"error": f"api_failure: {e}", "role": role, "turns_used": turn - 1,
                            "tool_log": tool_log, "cost": cost}
                time.sleep(2 * (attempt + 1))
        cost += c

        if response_text.startswith('{"__tool_calls__"'):
            if tool_protocol == "openai":
                # canonical OpenAI assistant-tool_calls message (Gemini adapter)
                clean_tcs = []
                for tc in tc_data.get("__tool_calls__", []):
                    fn = tc.get("function", {})
                    args = fn.get("arguments", "{}")
                    if not isinstance(args, str):
                        args = json.dumps(args)
                    clean_tcs.append({
                        "id": tc.get("id") or f"call_{turn}",
                        "type": "function",
                        "function": {"name": fn.get("name", ""), "arguments": args},
                    })
                messages.append({"role": "assistant", "content": None, "tool_calls": clean_tcs})
            else:
                messages.append({"role": "assistant", "content": response_text})
            tool_calls = tc_data.get("__tool_calls__", [])
        else:
            messages.append({"role": "assistant", "content": response_text})
            tool_calls = []
            messages.append({"role": "user", "content": "[Continue]"})

        for tc in tool_calls:
            fn_name = tc.get("function", {}).get("name", "")
            fn_args, malformed = _parse_args(tc.get("function", {}).get("arguments", "{}"))
            call_meta = {"turn": turn, "tool": fn_name, "args": fn_args,
                         "malformed": malformed, "ok": True, "note": None}

            if fn_name == "read_file":
                requested = fn_args.get("path", f"{entry_file}.py")
                call_meta["path_sanitized"] = ("/" in str(requested)) and (str(requested) != str(Path(requested).name))
                result = read_file_content(work_dir, requested)
            elif fn_name == "write_file":
                requested = fn_args.get("path", f"{entry_file}.py")
                call_meta["path_sanitized"] = ("/" in str(requested)) and (str(requested) != str(Path(requested).name))
                result = write_file_content(work_dir, requested, fn_args.get("content", ""))
            elif fn_name == "read_briefing":
                result = read_file_content(work_dir, "briefing.txt")
            elif fn_name == "run_tests":
                result = tests_feedback(work_dir, entry_file)
            elif fn_name == "finish":
                passed = grade_entry(work_dir, entry_file)
                messages.append({"role": "user", "content": "[Tool: finish]"})
                call_meta["result"] = "FINISHED"
                call_meta["ok"] = True
                tool_log.append(call_meta)
                return {"passed": passed, "role": role, "turns_used": turn, "messages": messages,
                        "tool_log": tool_log, "cost": cost,
                        "code": read_file_content(work_dir, f"{entry_file}.py")}
            else:
                call_meta["ok"] = False
                call_meta["note"] = "unknown_tool"
                result = f"Unknown tool: {fn_name}"

            if tool_protocol == "openai":
                # canonical OpenAI tool-call format (Gemini adapter):
                # results go in role-tool messages keyed by tool_call_id.
                tcid = tc.get("id") or f"call_{turn}_{fn_name}"
                messages.append({"role": "tool", "tool_call_id": tcid,
                                 "content": result[:3000]})
            else:
                messages.append({"role": "user", "content": f"[Tool: {fn_name}]\n{result[:3000]}"})
            call_meta["result"] = result[:300]
            tool_log.append(call_meta)

    passed = grade_entry(work_dir, entry_file)
    return {"passed": passed, "role": role, "turns_used": max_turns, "messages": messages,
            "tool_log": tool_log, "cost": cost,
            "code": read_file_content(work_dir, f"{entry_file}.py")}


# ---------------------------------------------------------------------------
# Briefing (CLEAN-style BRIEF-400, model-parameterized)
# ---------------------------------------------------------------------------

def make_brief(prob, a_code, test_results, seed, model) -> tuple[str, int, float]:
    prompt = BRIEF_PROMPT.format(entry_file=prob["name"], code=a_code, test_results=test_results)
    messages = [{"role": "system", "content": "You are helpful."},
                {"role": "user", "content": prompt}]
    text, toks, cost = call_with_retry(model, messages, temperature=0.3,
                                       max_tokens=2000, tools=None, seed=seed)
    if count_completion_tokens(text) > 400:
        text = text[:1600]
    return text, count_completion_tokens(text), cost


# ---------------------------------------------------------------------------
# Consumption coding (prereg b) — blind to outcome, tool sequence only
# ---------------------------------------------------------------------------

def code_consumption(b_tool_log, entry_file) -> dict:
    first_write = None
    first_read = None
    wrote_solution = False
    for i, c in enumerate(b_tool_log):
        if c["tool"] == "write_file" and (c["args"].get("path") or "") == f"{entry_file}.py":
            if first_write is None:
                first_write = i
            wrote_solution = True
        if c["tool"] == "read_briefing" and first_read is None:
            first_read = i
    if not wrote_solution:
        return {"verdict": "NO-SOLUTION-WRITE", "first_read_briefing": first_read, "first_solution_write": first_write}
    if first_read is not None and first_read < first_write:
        return {"verdict": "CONSUMED", "first_read_briefing": first_read, "first_solution_write": first_write}
    return {"verdict": "NOT-CONSUMED", "first_read_briefing": first_read, "first_solution_write": first_write}


# ---------------------------------------------------------------------------
# Tool-metadata summary (prereg d)
# ---------------------------------------------------------------------------

def tool_summary(tool_log) -> dict:
    counts = {}
    unknown = []
    malformed = 0
    sanitized = 0
    for c in tool_log:
        counts[c["tool"]] = counts.get(c["tool"], 0) + 1
        if c["note"] == "unknown_tool":
            unknown.append(c["tool"])
        if c.get("malformed"):
            malformed += 1
        if c.get("path_sanitized"):
            sanitized += 1
    order = [c["tool"] for c in tool_log]
    return {"counts": counts, "unknown_tools": sorted(set(unknown)),
            "malformed_args": malformed, "path_sanitized": sanitized,
            "call_order": order, "total_calls": len(tool_log)}


# ---------------------------------------------------------------------------
# Run one family x task
# ---------------------------------------------------------------------------

def run_one(family: str, prob: dict, seed: int, budget: dict) -> dict:
    model = FAMILIES[family]
    work_dir = RUN_DIR / family / f"{prob['name']}_s{seed}"
    if work_dir.exists():
        import shutil
        shutil.rmtree(work_dir)
    setup_workspace(prob, work_dir)
    spec = prob["prompt"]
    enf = prob["name"]
    # A workspace: canonical stub + test file (A's run_tests/grade are real)
    setup_workspace(prob, work_dir / "a")
    snapshot_tests(work_dir / "a", enf)

    # Agent A (writer, same family — self-pair transport)
    # Per-family adapter: Gemini uses canonical OpenAI tool messages (it
    # otherwise imitates the raw JSON history as truncated content).
    proto = "openai" if family == "gemini" else "json"
    a = run_agent(prob, f"## Task\n\n{spec}\n\nWrite your solution to {enf}.py.",
                  TURNS_A, work_dir / "a", seed, model, role="a", tool_protocol=proto)
    run_cost = a.get("cost", 0.0)
    budget["spent"] += run_cost
    if "error" in a:
        return {"family": family, "task": enf, "seed": seed, "model": model,
                "excluded": True, "error": a["error"], "a": a, "cost": run_cost}

    a_code = a["code"]
    test_results = tests_feedback(work_dir / "a", enf)
    a_passed = grade_entry(work_dir / "a", enf)

    # CLEAN-style briefing (no error, no cue)
    try:
        brief_text, brief_tokens, brief_cost = make_brief(prob, a_code, test_results, seed, model)
    except Exception as e:
        return {"family": family, "task": enf, "seed": seed, "model": model,
                "excluded": True, "error": f"brief_api_failure: {e}",
                "a": {k: a[k] for k in ("turns_used", "cost", "tool_log", "passed")},
                "cost": run_cost}
    run_cost += brief_cost
    budget["spent"] += brief_cost

    # B workspace: always start from the canonical stub+test workspace.
    # Inherit A's real solution only when A had NOT completed the task, so B
    # always has something to write (the consumption criterion needs a
    # solution-write to order against). A-complete runs test the briefing
    # mechanism, not a handoff of finished work. Stage-0 transport-only
    # adaptation; B's context below reflects B's actual file state.
    b_dir = work_dir / "b"
    b_dir.mkdir(parents=True, exist_ok=True)
    setup_workspace(prob, b_dir)
    a_sol_file = work_dir / "a" / f"{enf}.py"
    a_sol_content = a_sol_file.read_text() if a_sol_file.exists() else ""
    if (not a_passed) and a_sol_content:
        (b_dir / f"{enf}.py").write_text(a_sol_content)
    for f in (work_dir / "a").iterdir():
        if f.is_file() and f.suffix == ".py" and f.name not in (f"{enf}.py", f"test_{enf}.py"):
            (b_dir / f.name).write_text(f.read_text())
    snapshot_tests(b_dir, enf)
    (b_dir / "briefing.txt").write_text(brief_text)
    b_file_state = (b_dir / f"{enf}.py").read_text()

    # Agent B (receiver, same family)
    b_context = "\n".join([
        f"## Task\n\n{spec}",
        f"\n## Current file state\n\nCode in {enf}.py:\n```\n{b_file_state}\n```",
        "\n## Briefing from the previous agent\nA briefing written by the previous agent is stored in briefing.txt. You MUST read it with read_briefing before writing any solution code.",
        f"\nContinue from where the previous agent left off. Write a correct solution to {enf}.py.",
    ])
    b = run_agent(prob, b_context, TURNS_B, b_dir, seed, model, role="b",
                  tools=B_TOOLS, system_extra=B_SYSTEM_EXTRA, tool_protocol=proto)
    b_cost = b.get("cost", 0.0)
    run_cost += b_cost
    budget["spent"] += b_cost
    if "error" in b:
        return {"family": family, "task": enf, "seed": seed, "model": model,
                "excluded": True, "error": b["error"],
                "a": {k: a[k] for k in ("turns_used", "cost", "tool_log", "passed")},
                "brief": {"tokens": brief_tokens, "cost": brief_cost, "text": brief_text},
                "consumption": code_consumption(b["tool_log"], enf),
                "cost": run_cost}

    b_code = b["code"]
    b_passed = grade_entry(b_dir, enf)
    consumption = code_consumption(b["tool_log"], enf)
    transport_complete = (
        "error" not in a and "error" not in b
        and consumption["verdict"] == "CONSUMED"
        and consumption["first_solution_write"] is not None
    )

    return {
        "family": family, "task": enf, "seed": seed, "model": model,
        "excluded": False,
        "a": {"passed": a["passed"], "turns": a["turns_used"], "cost": a["cost"],
              "tool_summary": tool_summary(a["tool_log"])},
        "brief": {"tokens": brief_tokens, "cost": brief_cost, "text": brief_text},
        "b": {"passed": b_passed, "turns": b["turns_used"], "cost": b["cost"],
              "tool_summary": tool_summary(b["tool_log"]), "code": b_code},
        "a_passed_at_interrupt": a_passed,
        "consumption": consumption,
        "transport_complete": transport_complete,
        "cost": run_cost,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"spent": 0.0}
    results = []
    print(f"Stage 0 — 4 families x {len(STAGE0_TASKS)} tasks x seed {SEED} (self-pair, CLEAN brief)")
    print(f"Budget cap: ${BUDGET_CAP}\n")
    for family in FAMILIES:
        for prob in STAGE0_TASKS:
            # Resume: skip runs already logged (reruns of earlier families)
            log_dir = RUN_DIR / family
            run_file = log_dir / f"{prob['name']}_s{SEED}.json"
            if run_file.exists():
                try:
                    existing = json.loads(run_file.read_text())
                    if "excluded" in existing:
                        print(f"[{family:9s}] {prob['name']:18s} (cached)", flush=True)
                        results.append(existing)
                        continue
                except json.JSONDecodeError:
                    pass
            if budget["spent"] >= BUDGET_CAP:
                results.append({"family": family, "task": prob["name"], "seed": SEED,
                                "excluded": True, "error": "budget_exceeded", "cost": budget["spent"]})
                continue
            print(f"[{family:9s}] {prob['name']:18s} ...", flush=True)
            r = run_one(family, prob, SEED, budget)
            results.append(r)
            if r.get("excluded"):
                print(f"    EXCLUDED ({r.get('error', '')[:80]}) | spent=${budget['spent']:.4f}")
            else:
                print(f"    a_pass={r['a']['passed']} b_pass={r['b']['passed']} "
                      f"consumption={r['consumption']['verdict']} transport={r['transport_complete']} "
                      f"spent=${budget['spent']:.4f}")
            # write per-run log
            log_dir = RUN_DIR / family
            log_dir.mkdir(parents=True, exist_ok=True)
            (log_dir / f"{prob['name']}_s{SEED}.json").write_text(json.dumps(r, indent=2, default=str))

    out = RUN_DIR / "stage0_results.json"
    out.write_text(json.dumps({"budget_spent": round(budget["spent"], 4), "results": results}, indent=2, default=str))

    # Family summary
    print("\n" + "=" * 78)
    print(f"FAMILY SUMMARY (budget spent: ${budget['spent']:.4f})")
    print("=" * 78)
    for family in FAMILIES:
        fr = [r for r in results if r["family"] == family]
        complete = [r for r in fr if not r.get("excluded") and r["transport_complete"]]
        consumed = [r for r in fr if not r.get("excluded") and r["consumption"]["verdict"] == "CONSUMED"]
        excluded = [r for r in fr if r.get("excluded")]
        cost = sum(r.get("cost", 0) for r in fr)  # cumulative per-family approx (budget cumulative)
        print(f"\n{family} ({FAMILIES[family]})")
        for r in fr:
            if r.get("excluded"):
                print(f"  {r['task']:18s} EXCLUDED ({r.get('error', '')[:60]})")
            else:
                print(f"  {r['task']:18s} a_pass={r['a']['passed']} b_pass={r['b']['passed']} "
                      f"consumption={r['consumption']['verdict']:16s} transport_complete={r['transport_complete']}")
        verdict = "PASS" if len(complete) >= 4 else "FAIL"
        print(f"  -> transport-complete: {len(complete)}/5  consumed: {len(consumed)}/5  excluded: {len(excluded)}  verdict: {verdict}")
    print("\nResults: " + str(out))


if __name__ == "__main__":
    main()
