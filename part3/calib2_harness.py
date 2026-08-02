#!/usr/bin/env python3
"""part3/calib2_harness.py — Handoff Part III Round-2 hard-tier calibration.

Runs the Stage 0 transport harness over the 10 Round-2 candidates with
calibration seeds 555/666 (burned, outside {42,123,256,777,888}), self-pair,
CLEAN BRIEF-400 briefings, interrupt at the V3 convention (A turn 7 of 12,
B turn 5) — UNCHANGED from Round 1 per ruling 2 (difficulty first).

Retry policy per ruling 3: up to 5 attempts per API call
(s0.MAX_CALL_RETRIES = 4). API/schema failures still excludable; task
failures never.

Reuses stage0_harness.run_one by import; no existing files modified.
Usage: .venv/bin/python3 part3/calib2_harness.py [family]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE.parent))

import stage0_harness as s0  # noqa: E402
from calib2_tasks import CALIB2_TASKS  # noqa: E402

SEEDS = [555, 666]
BUDGET_CAP = 15.0
CALIB_DIR = BASE / "calib2_logs"
s0.RUN_DIR = CALIB_DIR  # route workspaces and logs to calib2_logs/
s0.MAX_CALL_RETRIES = 4  # ruling 3: up to 5 attempts per API call


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    families = [only] if only else list(s0.FAMILIES)
    CALIB_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"spent": 0.0}
    results = []
    for family in families:
        for seed in SEEDS:
            for prob in CALIB2_TASKS:
                log_dir = CALIB_DIR / family
                run_file = log_dir / f"{prob['name']}_s{seed}.json"
                if run_file.exists():
                    try:
                        existing = json.loads(run_file.read_text())
                        # Cache ALL completed runs (excluded or not); fold
                        # their cost into the budget so the aggregate reports
                        # the true spend and nothing is re-run/overwritten.
                        budget["spent"] += float(existing.get("cost", 0.0) or 0.0)
                        results.append(existing)
                        print(f"[{family:9s}] {prob['name']:26s} s{seed} (cached, cost=${float(existing.get('cost', 0.0)):.4f})", flush=True)
                        continue
                    except json.JSONDecodeError:
                        pass
                if budget["spent"] >= BUDGET_CAP:
                    results.append({"family": family, "task": prob["name"], "seed": seed,
                                    "excluded": True, "error": "budget_exceeded", "cost": budget["spent"]})
                    continue
                print(f"[{family:9s}] {prob['name']:26s} s{seed} ...", flush=True)
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
    out = CALIB_DIR / "calib2_results.json"
    out.write_text(json.dumps({"budget_spent": round(budget["spent"], 4), "results": results}, indent=2, default=str))
    print("wrote", out)


if __name__ == "__main__":
    main()
