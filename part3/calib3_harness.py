#!/usr/bin/env python3
"""part3/calib3_harness.py — Handoff Part III Round-3 hard-tier calibration.

Implements the Round-3 protocol per CALIBRATION3_PREREG.md (Buzz event
1885cf44 rulings 1-5):

- Ruling 1: A interrupted at turn 4 of a NOMINAL 8-turn budget (prompt says 8,
  harness stops at 4); B budget unchanged at 5 turns.
- Ruling 2: 11 tasks (4 Round-2 in-band survivors + 7 new B-fresh-solve-fails
  candidates), seeds 313/515 (burned), 20-80% band, tier of 8, STOP if <6.
- Ruling 3: malformed-payload retry — up to 3 retries per malformed tool call,
  each logged with the raw payload; honest-failure fallback.
- Ruling 4: gemini family representative = google/gemini-2.5-pro for all runs.
- Ruling 5: ledger items recorded in run records (retry_events, consumption
  verdicts, path_sanitized flags) for the confirmatory prereg.

Reuses stage0_harness helpers by import; no existing file modified.
Usage: .venv/bin/python3 part3/calib3_harness.py [family]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE.parent))

import stage0_harness as s0  # noqa: E402
from calib3_tasks import CALIB3_TASKS  # noqa: E402

SEEDS = [313, 515]
BUDGET_CAP = 25.0
CALIB_DIR = BASE / "calib3_logs"

# Ruling 1: A nominal 8-turn budget, interrupted at turn 4; B budget 5.
TURNS_A_NOMINAL = 8
TURNS_A_INTERRUPT = 4
TURNS_B = 5

# Ruling 4: gemini family representative effective immediately.
s0.FAMILIES["gemini"] = "google/gemini-2.5-pro"

# Retry policies: API/schema up to 5 attempts (Round-2 ruling 3);
# ruling 3: malformed-payload retry up to 3.
s0.MAX_CALL_RETRIES = 4
MALFORMED_RETRIES = 3


def run_agent(prob, init_context, work_dir, seed, model, role,
              nominal_turns, loop_turns, tools=None, system_extra="",
              tool_protocol="json"):
    """Run one agent with a nominal turn budget (prompt) and a possibly
    earlier interrupt point (loop bound). Ruling-3 malformed-payload retry:
    a response whose tool-call names are not in the known registry is
    re-requested up to MALFORMED_RETRIES times with the SAME message state;
    each retry is logged with the raw payload. If still malformed, the turn
    is consumed as an honest unknown-tool failure.
    """
    entry_file = prob["name"]
    work_dir.mkdir(parents=True, exist_ok=True)
    system = s0.SYSTEM_PROMPT_TEMPLATE.format(
        entry_file=entry_file, max_turns=nominal_turns) + system_extra
    messages = [{"role": "system", "content": system},
                {"role": "user", "content": init_context}]
    tool_log = []
    retry_events = []
    cost = 0.0
    toolset = tools or s0.TOOLS

    def call_api():
        # Returns (response_text, cost) on success, (None, exception) on
        # exhausted API/schema retries (excludable failure).
        for attempt in range(s0.MAX_CALL_RETRIES + 1):
            try:
                resp, toks, c = s0.call_with_retry(
                    model, messages, temperature=0.3, max_tokens=4096,
                    tools=toolset, seed=seed)
                return resp, c
            except (s0.APIFailure, json.JSONDecodeError) as e:
                if attempt >= s0.MAX_CALL_RETRIES:
                    return None, e
                time.sleep(2 * (attempt + 1))
        return None, RuntimeError("unreachable")

    def _parse_resp(text):
        # Returns (tc_data_or_None, tool_calls, bad_names)
        if not text.startswith('{"__tool_calls__"'):
            return None, [], []
        try:
            tc_data = json.loads(text)
        except json.JSONDecodeError:
            return None, [], ["__invalid_json__"]
        calls = tc_data.get("__tool_calls__", [])
        bad = [tc.get("function", {}).get("name", "")
               for tc in calls if tc.get("function", {}).get("name", "") not in s0.KNOWN_TOOLS]
        return tc_data, calls, bad

    for turn in range(1, loop_turns + 1):
        response_text, c = call_api()
        if response_text is None:
            return {"error": f"api_failure: {c}", "role": role,
                    "turns_used": turn - 1, "tool_log": tool_log,
                    "retry_events": retry_events, "cost": cost}
        cost += c

        tc_data, tool_calls, bad = _parse_resp(response_text)

        # Ruling 3: malformed-payload retry loop (up to MALFORMED_RETRIES)
        retry_n = 0
        while bad and retry_n < MALFORMED_RETRIES:
            retry_n += 1
            retry_events.append({"turn": turn, "retry": retry_n,
                                 "bad_names": bad,
                                 "raw_payload": tool_calls if tc_data is not None else response_text[:1500]})
            time.sleep(1.0)
            response_text, c = call_api()
            if response_text is None:
                return {"error": f"api_failure: {c}", "role": role,
                        "turns_used": turn - 1, "tool_log": tool_log,
                        "retry_events": retry_events, "cost": cost}
            cost += c
            tc_data, tool_calls, bad = _parse_resp(response_text)

        if not tool_calls:
            # plain-text response (original or after retries): consume as text turn
            messages.append({"role": "assistant", "content": response_text})
            messages.append({"role": "user", "content": "[Continue]"})
            continue

        # append assistant message per protocol
        if tool_protocol == "openai":
            clean_tcs = []
            for tc in tool_calls:
                fn = tc.get("function", {})
                args = fn.get("arguments", "{}")
                if not isinstance(args, str):
                    args = json.dumps(args)
                clean_tcs.append({"id": tc.get("id") or f"call_{turn}",
                                  "type": "function",
                                  "function": {"name": fn.get("name", ""), "arguments": args}})
            messages.append({"role": "assistant", "content": None, "tool_calls": clean_tcs})
        else:
            messages.append({"role": "assistant", "content": response_text})

        for tc in tool_calls:
            fn_name = tc.get("function", {}).get("name", "")
            fn_args, malformed = s0._parse_args(tc.get("function", {}).get("arguments", "{}"))
            call_meta = {"turn": turn, "tool": fn_name, "args": fn_args,
                         "malformed": malformed, "ok": True, "note": None}

            if fn_name == "read_file":
                requested = fn_args.get("path", f"{entry_file}.py")
                call_meta["path_sanitized"] = ("/" in str(requested)) and (str(requested) != str(Path(requested).name))
                result = s0.read_file_content(work_dir, requested)
            elif fn_name == "write_file":
                requested = fn_args.get("path", f"{entry_file}.py")
                call_meta["path_sanitized"] = ("/" in str(requested)) and (str(requested) != str(Path(requested).name))
                result = s0.write_file_content(work_dir, requested, fn_args.get("content", ""))
            elif fn_name == "read_briefing":
                result = s0.read_file_content(work_dir, "briefing.txt")
            elif fn_name == "run_tests":
                result = s0.tests_feedback(work_dir, entry_file)
            elif fn_name == "finish":
                passed = s0.grade_entry(work_dir, entry_file)
                messages.append({"role": "user", "content": "[Tool: finish]"})
                call_meta["result"] = "FINISHED"
                call_meta["ok"] = True
                tool_log.append(call_meta)
                return {"passed": passed, "role": role, "turns_used": turn,
                        "messages": messages, "tool_log": tool_log,
                        "retry_events": retry_events, "cost": cost,
                        "code": s0.read_file_content(work_dir, f"{entry_file}.py")}
            else:
                call_meta["ok"] = False
                call_meta["note"] = "unknown_tool"
                result = f"Unknown tool: {fn_name}"

            if tool_protocol == "openai":
                tcid = tc.get("id") or f"call_{turn}_{fn_name}"
                messages.append({"role": "tool", "tool_call_id": tcid,
                                 "content": result[:3000]})
            else:
                messages.append({"role": "user", "content": f"[Tool: {fn_name}]\n{result[:3000]}"})
            call_meta["result"] = result[:300]
            tool_log.append(call_meta)

    passed = s0.grade_entry(work_dir, entry_file)
    return {"passed": passed, "role": role, "turns_used": loop_turns,
            "messages": messages, "tool_log": tool_log,
            "retry_events": retry_events, "cost": cost,
            "code": s0.read_file_content(work_dir, f"{entry_file}.py")}


def run_one(family: str, prob: dict, seed: int, budget: dict) -> dict:
    model = s0.FAMILIES[family]
    enf = prob["name"]
    work_dir = CALIB_DIR / family / f"{enf}_s{seed}"
    if work_dir.exists():
        import shutil
        shutil.rmtree(work_dir)
    s0.setup_workspace(prob, work_dir)
    spec = prob["prompt"]
    s0.setup_workspace(prob, work_dir / "a")
    s0.snapshot_tests(work_dir / "a", enf)

    proto = "openai" if family == "gemini" else "json"
    a = run_agent(prob, f"## Task\n\n{spec}\n\nWrite your solution to {enf}.py.",
                  work_dir / "a", seed, model, role="a",
                  nominal_turns=TURNS_A_NOMINAL, loop_turns=TURNS_A_INTERRUPT,
                  tool_protocol=proto)
    run_cost = a.get("cost", 0.0)
    budget["spent"] += run_cost
    if "error" in a:
        return {"family": family, "task": enf, "seed": seed, "model": model,
                "excluded": True, "error": a["error"], "a": a, "cost": run_cost}

    a_code = a["code"]
    test_results = s0.tests_feedback(work_dir / "a", enf)
    a_passed = s0.grade_entry(work_dir / "a", enf)

    try:
        brief_text, brief_tokens, brief_cost = s0.make_brief(prob, a_code, test_results, seed, model)
    except Exception as e:
        return {"family": family, "task": enf, "seed": seed, "model": model,
                "excluded": True, "error": f"brief_api_failure: {e}",
                "a": {k: a[k] for k in ("turns_used", "cost", "tool_log", "passed", "retry_events") if k in a},
                "cost": run_cost}
    run_cost += brief_cost
    budget["spent"] += brief_cost

    # B workspace: A-complete rule (CHANGELOG entry 1) unchanged.
    b_dir = work_dir / "b"
    b_dir.mkdir(parents=True, exist_ok=True)
    s0.setup_workspace(prob, b_dir)
    a_sol_file = work_dir / "a" / f"{enf}.py"
    a_sol_content = a_sol_file.read_text() if a_sol_file.exists() else ""
    if (not a_passed) and a_sol_content:
        (b_dir / f"{enf}.py").write_text(a_sol_content)
    for f in (work_dir / "a").iterdir():
        if f.is_file() and f.suffix == ".py" and f.name not in (f"{enf}.py", f"test_{enf}.py"):
            (b_dir / f.name).write_text(f.read_text())
    s0.snapshot_tests(b_dir, enf)
    (b_dir / "briefing.txt").write_text(brief_text)
    b_file_state = (b_dir / f"{enf}.py").read_text()

    b_context = "\n".join([
        f"## Task\n\n{spec}",
        f"\n## Current file state\n\nCode in {enf}.py:\n```\n{b_file_state}\n```",
        "\n## Briefing from the previous agent\nA briefing written by the previous agent is stored in briefing.txt. You MUST read it with read_briefing before writing any solution code.",
        f"\nContinue from where the previous agent left off. Write a correct solution to {enf}.py.",
    ])
    b = run_agent(prob, b_context, b_dir, seed, model, role="b",
                  nominal_turns=TURNS_B, loop_turns=TURNS_B,
                  tools=s0.B_TOOLS, system_extra=s0.B_SYSTEM_EXTRA,
                  tool_protocol=proto)
    b_cost = b.get("cost", 0.0)
    run_cost += b_cost
    budget["spent"] += b_cost
    if "error" in b:
        return {"family": family, "task": enf, "seed": seed, "model": model,
                "excluded": True, "error": b["error"],
                "a": {k: a[k] for k in ("turns_used", "cost", "tool_log", "passed", "retry_events") if k in a},
                "b": {k: b[k] for k in ("turns_used", "cost", "tool_log", "retry_events") if k in b},
                "brief": {"tokens": brief_tokens, "cost": brief_cost, "text": brief_text},
                "consumption": s0.code_consumption(b["tool_log"], enf),
                "cost": run_cost}

    b_code = b["code"]
    b_passed = s0.grade_entry(b_dir, enf)
    consumption = s0.code_consumption(b["tool_log"], enf)
    transport_complete = (
        "error" not in a and "error" not in b
        and consumption["verdict"] == "CONSUMED"
        and consumption["first_solution_write"] is not None
    )

    return {
        "family": family, "task": enf, "seed": seed, "model": model,
        "excluded": False,
        "a": {"passed": a["passed"], "turns": a["turns_used"], "cost": a["cost"],
              "tool_summary": s0.tool_summary(a["tool_log"]),
              "retry_events": a["retry_events"]},
        "brief": {"tokens": brief_tokens, "cost": brief_cost, "text": brief_text},
        "b": {"passed": b_passed, "turns": b["turns_used"], "cost": b["cost"],
              "tool_summary": s0.tool_summary(b["tool_log"]),
              "retry_events": b["retry_events"], "code": b_code},
        "a_passed_at_interrupt": a_passed,
        "consumption": consumption,
        "transport_complete": transport_complete,
        "cost": run_cost,
    }


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    families = [only] if only else list(s0.FAMILIES)
    CALIB_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"spent": 0.0}
    results = []
    for family in families:
        for seed in SEEDS:
            for prob in CALIB3_TASKS:
                log_dir = CALIB_DIR / family
                run_file = log_dir / f"{prob['name']}_s{seed}.json"
                if run_file.exists():
                    try:
                        existing = json.loads(run_file.read_text())
                        budget["spent"] += float(existing.get("cost", 0.0) or 0.0)
                        results.append(existing)
                        print(f"[{family:9s}] {prob['name']:22s} s{seed} (cached, cost=${float(existing.get('cost', 0.0)):.4f})", flush=True)
                        continue
                    except json.JSONDecodeError:
                        pass
                if budget["spent"] >= BUDGET_CAP:
                    results.append({"family": family, "task": prob["name"], "seed": seed,
                                    "excluded": True, "error": "budget_exceeded", "cost": budget["spent"]})
                    continue
                print(f"[{family:9s}] {prob['name']:22s} s{seed} ...", flush=True)
                r = run_one(family, prob, seed, budget)
                results.append(r)
                if r.get("excluded"):
                    print(f"    EXCLUDED ({str(r.get('error', ''))[:80]}) spent=${budget['spent']:.4f}", flush=True)
                else:
                    print(f"    a_pass={r['a']['passed']} b_pass={r['b']['passed']} "
                          f"cons={r['consumption']['verdict']} A_complete={r['a_passed_at_interrupt']} "
                          f"spent=${budget['spent']:.4f}", flush=True)
                log_dir.mkdir(parents=True, exist_ok=True)
                (log_dir / f"{prob['name']}_s{seed}.json").write_text(json.dumps(r, indent=2, default=str))
    out = CALIB_DIR / "calib3_results.json"
    out.write_text(json.dumps({"budget_spent": round(budget["spent"], 4), "results": results}, indent=2, default=str))
    print("wrote", out)


if __name__ == "__main__":
    main()
