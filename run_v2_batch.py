#!/usr/bin/env python3
"""
Batch runner for handoff_v2.py — saves progress after each run, resumes on restart.
Runs each condition as a subprocess with timeout for robustness.
Run: python3 -u run_v2_batch.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handoff_v2 as v2

DATA_DIR = Path(__file__).resolve().parent / "data_v2"
PROGRESS_FILE = DATA_DIR / "_progress.json"
RESULTS_FILE = DATA_DIR / "results.json"
CONDITIONS = ["continuous", "raw", "brief", "wake", "no_handoff"]
RUN_TIMEOUT = 600  # 10 minutes per run


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"completed": [], "results": []}


def save_progress(completed: list, results: list):
    PROGRESS_FILE.write_text(json.dumps({
        "completed": completed,
        "results": [{k: v for k, v in r.items() if k not in ("a_log", "b_log", "a_code", "b_code", "handoff")} for r in results],
    }, indent=2))


def build_run_key(seed: int, prob_name: str, cond: str) -> str:
    return f"{prob_name}_{cond}_s{seed}"


def run_single(seed: int, prob_name: str, cond: str) -> dict | None:
    """Run a single condition as a subprocess using handoff_v2.py run_single."""
    python = v2.VENV_PYTHON if Path(v2.VENV_PYTHON).exists() else "python3"
    script_path = Path(__file__).resolve().parent / "handoff_v2.py"
    cmd = [python, str(script_path), "run_single", cond, prob_name, str(seed)]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=RUN_TIMEOUT,
            cwd=str(Path(__file__).resolve().parent)
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line.startswith('RESULT:'):
                    return json.loads(line[7:])
            # No RESULT: line found (maybe print only)
            print(f"  No result marker in output", flush=True)
            return None
        else:
            err = result.stderr.strip()[:500] if result.stderr.strip() else "Unknown error"
            print(f"  SUBPROCESS ERROR: {err}", flush=True)
            return None
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT after {RUN_TIMEOUT}s", flush=True)
        return None
    except Exception as e:
        print(f"  SUBPROCESS EXCEPTION: {e}", flush=True)
        return None


def main():
    progress = load_progress()
    completed_set = set(progress["completed"])
    all_results = progress["results"]

    runs = [
        (seed, prob, cond)
        for seed in v2.SEEDS
        for prob in v2.HARD_PROBLEMS
        for cond in CONDITIONS
    ]

    total = len(runs)
    done = len(completed_set)

    print(f"=== Handoff V2 Batch Runner ===")
    print(f"Total runs: {total}, Already done: {done}, Remaining: {total - done}")
    print(f"Seeds: {v2.SEEDS}")
    print(f"Problems: {[p['name'] for p in v2.HARD_PROBLEMS]}")
    print(f"Conditions: {CONDITIONS}")
    print(f"Progress file: {PROGRESS_FILE}")
    print(f"Results file: {RESULTS_FILE}")
    print()

    for idx, (seed, prob, cond) in enumerate(runs):
        key = build_run_key(seed, prob["name"], cond)
        if key in completed_set:
            continue

        print(f"[{done+1}/{total}] {prob['name']:20s} {cond:15s} seed={seed}", flush=True)

        # Run with 1 retry
        r = None
        for attempt in range(2):
            if attempt > 0:
                print(f"  Retry {attempt}...", flush=True)
                time.sleep(5)
            r = run_single(seed, prob["name"], cond)
            if r is not None:
                break

        if r is not None:
            result_compact = {k: r[k] for k in ("task_id", "condition", "passed", "a_turns", "b_turns", "handoff_tokens", "seed")}
            if r.get("raw_truncation_chars"):
                result_compact["raw_truncation_chars"] = r["raw_truncation_chars"]
            all_results.append(result_compact)
            print(f"  {'PASS' if r['passed'] else 'FAIL'} | A:{r['a_turns']} B:{r['b_turns']} hoff:{r['handoff_tokens']}", flush=True)
        else:
            result_compact = {
                "task_id": f"handoff/{prob['name']}",
                "condition": cond,
                "passed": False,
                "a_turns": -1,
                "b_turns": -1,
                "handoff_tokens": -1,
                "seed": seed,
                "error": "failed after 2 attempts",
            }
            all_results.append(result_compact)
            print(f"  FAIL (error)", flush=True)

        completed_set.add(key)
        done += 1
        save_progress(list(completed_set), all_results)

    # Save final compact results
    RESULTS_FILE.write_text(json.dumps(all_results, indent=2))
    print(f"\nFinal results saved to {RESULTS_FILE}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    by_cond = defaultdict(list)
    for r in all_results:
        if "condition" in r:
            by_cond[r["condition"]].append(r.get("passed", False))
    for c in CONDITIONS:
        p = by_cond[c]
        if p:
            print(f"  {c:15s}: {sum(p)}/{len(p)} ({100*sum(p)//len(p)}%)")
    print(f"  Total: {len(all_results)} runs, {sum(1 for r in all_results if r.get('passed', False))} passed")


if __name__ == "__main__":
    main()
