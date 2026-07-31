#!/usr/bin/env python3
"""H->H BRIEF-400 spot-check with the current (post-fix) harness.

Per Claude's comparability guard: the H->H cell in Experiment A was reused
from V2 data produced by the pre-fix harness. Rerun 2 tasks x 3 seeds with
the current harness and compare to V2's brief cell (16/24 = 66.7%).

Tasks chosen for maximum signal: median_two_sorted (2/3 in V2, and the task
that hit both mid-A harness bugs) and n_queens (0/3 in V2, hardest task).

Usage: nohup python3 run_hh_spotcheck.py > hh_spotcheck.log 2>&1 &
"""
from __future__ import annotations

import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
TASKS = ["median_two_sorted", "n_queens"]
SEEDS = [42, 123, 256]
OUT = BASE / "data_v3a_spotcheck"
OUT.mkdir(exist_ok=True)
PROG_FILE = OUT / "_progress.json"


def run_one(task: str, seed: int) -> dict:
    cmd = [sys.executable, "handoff_v3.py", "run_single", "a", "h_to_h", task, str(seed)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "task_id": f"handoff/{task}", "seed": seed}
    for line in res.stdout.split("\n"):
        if line.startswith("RESULT:"):
            return json.loads(line[7:])
    return {"error": (res.stderr or res.stdout)[-500:], "task_id": f"handoff/{task}", "seed": seed}


def main() -> None:
    prog = {"completed": [], "results": []}
    if PROG_FILE.exists():
        prog = json.loads(PROG_FILE.read_text())
    done = {f"{r.get('task_id', '').split('/')[-1]}_s{r.get('seed')}" for r in prog["results"]}
    jobs = [(t, s) for t in TASKS for s in SEEDS if f"{t}_s{s}" not in done]
    if not jobs:
        print("all spot-check runs already present")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(run_one, t, s): (t, s) for t, s in jobs}
        for fut in concurrent.futures.as_completed(futs):
            t, s = futs[fut]
            r = fut.result()
            key = f"{t}_s{s}"
            if "error" in r:
                print(f"{key}: ERROR {r['error'][:300]}", flush=True)
            else:
                print(f"{key}: {'PASS' if r['passed'] else 'FAIL'} "
                      f"A:{r['a_turns']} B:{r['b_turns']} hoff:{r['handoff_tokens']}", flush=True)
                prog["results"].append(r)
            prog["completed"].append(key)
            PROG_FILE.write_text(json.dumps(prog, indent=2))
    n = len(prog["results"])
    p = sum(1 for r in prog["results"] if r.get("passed"))
    print(f"\n=== H->H spot-check: {p}/{n} ({100 * p // n if n else 0}%) "
          f"vs V2 brief 16/24 (66.7%) ===", flush=True)


if __name__ == "__main__":
    main()
