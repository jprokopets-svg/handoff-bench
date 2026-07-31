#!/usr/bin/env python3
"""Batch runner for handoff_v3.py — saves progress, resumes on restart.

Usage: python3 run_v3_batch.py [a|b|all]
"""
import json
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA_A = BASE / "data_v3a"
DATA_B = BASE / "data_v3b"
PROGRESS_A = DATA_A / "_progress.json"
PROGRESS_B = DATA_B / "_progress.json"

SEEDS = [42, 123, 256]
TASKS = ["regex_parser", "n_queens", "median_stream", "word_break",
         "median_two_sorted", "serialize_tree", "max_path_sum", "merge_k_lists"]

# Experiment A cells (H→H reused from V2, not run)
CELLS_A = {"s_to_s": ("s", "s"), "s_to_h": ("s", "h"), "h_to_s": ("h", "s")}
# Experiment B cells
CELLS_B = {"subtle": ("subtle",), "flagged": ("flagged",)}
# Condition strings must match handoff_v3.py's run_pair/run_single stamps
CONDITION_MAP = {"s_to_s": "stos", "s_to_h": "stoh", "h_to_s": "htos",
                 "subtle": "htoh_subtle", "flagged": "htoh_flagged"}


def load_progress(path):
    if path.exists():
        return json.loads(path.read_text())
    return {"completed": [], "results": []}


def save_progress(path, prog):
    path.write_text(json.dumps(prog, indent=2))


def run_cell(exp, cell, task, seed, progress_file):
    """Run one cell; returns (ok, result_json_str, error)."""
    cmd = [sys.executable, "handoff_v3.py", "run_single", exp, cell, task, str(seed)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return False, None, "timeout"
    if res.returncode != 0:
        return False, None, res.stderr.strip()[-500:] or res.stdout.strip()[-500:]
    for line in res.stdout.split("\n"):
        if line.startswith("RESULT:"):
            return True, line[7:], None
    return False, None, "no RESULT marker"


def run_batch(exp):
    if exp == "a":
        cells, data_dir, progress_file, key_prefix = CELLS_A, DATA_A, PROGRESS_A, "v3a"
    else:
        cells, data_dir, progress_file, key_prefix = CELLS_B, DATA_B, PROGRESS_B, "v3b"

    data_dir.mkdir(parents=True, exist_ok=True)
    prog = load_progress(progress_file)
    completed = set(prog["completed"])

    total = len(cells) * len(TASKS) * len(SEEDS)
    done_before = len(prog["completed"])
    print(f"=== V3 Experiment {exp.upper()} ===")
    print(f"Total: {total}, already done: {done_before}, remaining: {total - done_before}")

    run_num = done_before
    for cell in cells:
        for task in TASKS:
            for seed in SEEDS:
                key = f"{task}_{cell}_s{seed}"
                if key in completed:
                    continue
                run_num += 1
                print(f"[{run_num}/{total}] {task:20s} {cell:10s} seed={seed}", flush=True)

                # Clean partial work dir
                work_dir = data_dir / key
                if work_dir.exists():
                    import shutil
                    shutil.rmtree(work_dir)

                ok, result_json, err = run_cell(exp, cell, task, seed, progress_file)
                if ok:
                    try:
                        r = json.loads(result_json)
                        status = "PASS" if r.get("passed") else "FAIL"
                        det = ""
                        if r.get("detected") is not None:
                            det = f" detected={r['detected']} ({r.get('injection_type')})"
                        print(f"  {status} | A:{r['a_turns']} B:{r['b_turns']} hoff:{r['handoff_tokens']}{det}", flush=True)
                        prog["completed"].append(key)
                        prog["results"].append(r)
                    except json.JSONDecodeError:
                        err = "bad result json"
                        ok = False
                if not ok:
                    print(f"  ERROR: {err}", flush=True)
                    prog["completed"].append(key)
                    prog["results"].append({
                        "task_id": f"handoff/{task}", "condition": CONDITION_MAP.get(cell, cell),
                        "passed": False, "a_turns": -1, "b_turns": -1,
                        "handoff_tokens": -1, "seed": seed, "error": err,
                    })
                save_progress(progress_file, prog)
                time.sleep(1)

    # Summary
    results = prog["results"]
    from collections import defaultdict
    by_cell = defaultdict(lambda: [0, 0])
    for r in results:
        cond = r.get("condition", r.get("condition", ""))
        key_cond = r.get("condition", "")
        by_cell[key_cond][1] += 1
        if r.get("passed"):
            by_cell[key_cond][0] += 1
    print(f"\n=== Experiment {exp.upper()} summary ===")
    for c in sorted(by_cell):
        p, t = by_cell[c]
        print(f"  {c:20s}: {p}/{t} ({100*p//t if t else 0}%)")
    print(f"Total: {len(results)} runs")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("a", "all"):
        run_batch("a")
    if which in ("b", "all"):
        run_batch("b")
