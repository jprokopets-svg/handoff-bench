#!/usr/bin/env python3
"""part3/calib_harness.py — Handoff Part III hard-tier calibration run.

Runs the Stage 0 transport harness over the 12 calibration candidates with
calibration seeds 777/888 (burned, outside {42,123,256}), self-pair, CLEAN
BRIEF-400 briefings, interrupt at the V3 convention (A turn 7 of 12, B turn 5).
Task selection is blind to experimental condition (no cue, no error).

Reuses stage0_harness.run_one by import; no existing files modified.

Usage: .venv/bin/python3 part3/calib_harness.py [family]
       (family optional: run a single family; omitting runs all four)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE.parent))

import stage0_harness as s0  # noqa: E402
from calib_tasks import CALIB_TASKS  # noqa: E402

SEEDS = [777, 888]
BUDGET_CAP = 15.0
CALIB_DIR = BASE / "calib_logs"
s0.RUN_DIR = CALIB_DIR  # route workspaces and logs to calib_logs/


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    families = [only] if only else list(s0.FAMILIES)
    CALIB_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"spent": 0.0}
    results = []
    for family in families:
        for seed in SEEDS:
            for prob in CALIB_TASKS:
                log_dir = CALIB_DIR / family
                run_file = log_dir / f"{prob['name']}_s{seed}.json"
                if run_file.exists():
                    try:
                        existing = json.loads(run_file.read_text())
                        # Cache ALL completed runs (excluded or not), not just
                        # excluded ones: re-running a completed run would
                        # overwrite its log and re-spend its cost. Cached cost
                        # is folded into the budget so the aggregate reports
                        # the true spend.
                        budget["spent"] += float(existing.get("cost", 0.0) or 0.0)
                        results.append(existing)
                        print(f"[{family:9s}] {prob['name']:28s} s{seed} (cached, cost=${float(existing.get('cost', 0.0)):.4f})", flush=True)
                        continue
                    except json.JSONDecodeError:
                        pass
                if budget["spent"] >= BUDGET_CAP:
                    results.append({"family": family, "task": prob["name"], "seed": seed,
                                    "excluded": True, "error": "budget_exceeded", "cost": budget["spent"]})
                    continue
                print(f"[{family:9s}] {prob['name']:28s} s{seed} ...", flush=True)
                r = s0.run_one(family, prob, seed, budget)
                results.append(r)
                if r.get("excluded"):
                    print(f"    EXCLUDED ({str(r.get('error', ''))[:80]}) spent=${budget['spent']:.4f}", flush=True)
                else:
                    print(f"    a_pass={r['a']['passed']} b_pass={r['b']['passed']} "
                          f"cons={r['consumption']['verdict']} transport={r['transport_complete']} "
                          f"A_complete={r['a_passed_at_interrupt']} spent=${budget['spent']:.4f}", flush=True)
                log_dir.mkdir(parents=True, exist_ok=True)
                (log_dir / f"{prob['name']}_s{seed}.json").write_text(json.dumps(r, indent=2, default=str))
    out = CALIB_DIR / "calib_results.json"
    out.write_text(json.dumps({"budget_spent": round(budget["spent"], 4), "results": results}, indent=2, default=str))
    print("wrote", out)


if __name__ == "__main__":
    main()
