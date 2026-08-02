#!/usr/bin/env python3
"""part3/calib2_gemini_sidetest.py — Round-2 Gemini model-specificity side-test.

Per ruling 3 and CALIBRATION2_PREREG.md: run the full transport loop on
2 Round-1 failing (task, seed) inputs with the baseline gemini-2.5-flash and
two alternative Gemini-family models. Determines whether the ~38% Round-1
run-loss (degenerate empty responses) is model-specific, and predeclares the
family-representative adapter decision for the confirmatory stage.

Models: baseline google/gemini-2.5-flash; alt1 google/gemini-2.5-pro;
alt2 google/gemini-3-flash-preview. Inputs: course_schedule s777 and
decode_string s777 (Round-1 exclusions). Logs isolated under
part3/calib2_logs/side_test/<model>/.

Usage: .venv/bin/python3 part3/calib2_gemini_sidetest.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE.parent))

import stage0_harness as s0  # noqa: E402
from calib_tasks import CALIB_TASKS  # noqa: E402 (Round-1 task defs)

BASELINE = "google/gemini-2.5-flash"
ALTS = ["google/gemini-2.5-pro", "google/gemini-3-flash-preview"]
MODELS = [BASELINE] + ALTS
INPUTS = [("course_schedule", 777), ("decode_string", 777)]

SIDE_DIR = BASE / "calib2_logs" / "side_test"


def main():
    SIDE_DIR.mkdir(parents=True, exist_ok=True)
    tasks = {t["name"]: t for t in CALIB_TASKS}
    s0.MAX_CALL_RETRIES = 4  # same retry policy as the main Round-2 run
    results = []
    budget = {"spent": 0.0}
    for model in MODELS:
        saved = s0.FAMILIES["gemini"]
        s0.FAMILIES["gemini"] = model
        for task_name, seed in INPUTS:
            prob = tasks[task_name]
            run_dir = SIDE_DIR / model.replace("/", "__")
            s0.RUN_DIR = run_dir
            run_file = run_dir / f"{task_name}_s{seed}.json"
            if run_file.exists():
                try:
                    existing = json.loads(run_file.read_text())
                    budget["spent"] += float(existing.get("cost", 0.0) or 0.0)
                    results.append(existing)
                    print(f"[{model:30s}] {task_name:20s} s{seed} (cached)", flush=True)
                    continue
                except json.JSONDecodeError:
                    pass
            print(f"[{model:30s}] {task_name:20s} s{seed} ...", flush=True)
            r = s0.run_one("gemini", prob, seed, budget)
            results.append(r)
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / f"{task_name}_s{seed}.json").write_text(json.dumps(r, indent=2, default=str))
            status = f"EXCLUDED ({str(r.get('error', ''))[:70]})" if r.get("excluded") else \
                f"completed a_pass={r['a']['passed']} b_pass={r['b']['passed']} cons={r['consumption']['verdict']}"
            print(f"    {status} spent=${budget['spent']:.4f}", flush=True)
        s0.FAMILIES["gemini"] = saved

    out = SIDE_DIR / "side_test_results.json"
    out.write_text(json.dumps({"budget_spent": round(budget["spent"], 4), "results": results}, indent=2, default=str))
    print("\nwrote", out)

    # Predeclared decision rule (prereg): an alternative transports reliably
    # iff it completes the full transport loop on 2/2 inputs.
    print("\n--- verdicts ---")
    for model in MODELS:
        rs = [r for r in results if r["model"] == model]
        ok = sum(1 for r in rs if not r.get("excluded"))
        print(f"{model:30s} {ok}/{len(rs)} completed {'RELIABLE' if ok == len(rs) == 2 else 'not-reliable'}")
    rel = [m for m in ALTS if sum(1 for r in results if r["model"] == m and not r.get("excluded")) == 2]
    if rel:
        print(f"\nFAMILY-REPRESENTATIVE DECISION: {rel[0]} transports reliably on the failing inputs -> "
              f"predeclared as the Gemini family representative for the confirmatory stage (per-family adapter decision).")
    else:
        print("\nFAMILY-REPRESENTATIVE DECISION: no alternative transported reliably on the failing inputs -> "
              "feasibility finding; report before any confirmatory prereg.")


if __name__ == "__main__":
    main()
