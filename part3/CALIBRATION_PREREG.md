# Handoff Part III — Hard-Tier Calibration (Pre-registered)

Author: Claude (design), Pi (execution). Committed before any calibration code or runs, per hard-tier calibration authorization (Buzz event 64cc8605). Budget cap: $15. Scope: handoff-bench repo, part3 branch only.

## Purpose
Select the hard task tier for the confirmatory 2x2 factorial by measuring pooled cross-family executable success under CLEAN handoff conditions. Task selection is thereby blind to experimental condition: calibration runs use CLEAN briefings only — no verification cue, no planted error.

## Candidate task list (12)
Defined in `part3/calib_tasks.py`; materially harder than V2 (multi-function, edge-case-dense, or stateful); disjoint from the V2 task set and from the 5 Stage 0 tasks:

1. `atoi_clone` — string-to-int with sign/whitespace/overflow clamping (edge-case-dense)
2. `longest_substring_no_repeat` — sliding-window uniqueness
3. `max_area_container` — two-pointer container area maximization
4. `interval_merge` — overlapping-interval merge (adjacency + containment)
5. `rotate_image` — in-place 90-degree matrix rotation
6. `valid_bst` — BST validity with strict integer-bound semantics (multi-function)
7. `lru_cache` — LRU cache class with capacity edge cases (stateful)
8. `trie_impl` — Trie insert/search/startsWith (stateful)
9. `decode_string` — nested `k[string]` decoding with multi-digit counts (stack)
10. `course_schedule` — prerequisite-graph cycle detection (graph)
11. `min_window_substring` — minimum covering window
12. `find_duplicate_number` — duplicate detection in an n+1 array of [1,n]

## Protocol
- CLEAN BRIEF-400 briefing per run only (no cue, no error); selection blind to experimental condition.
- Self-pair transport per family (A = B = family), matching Stage 0; interrupt at the V3 convention: A at turn 7 of 12, B at turn 5.
- **Calibration seeds: 777 and 888** — both outside the confirmatory seed set {42, 123, 256}; thereby burned and excluded from confirmation.
- 4 families x 12 candidates x 2 seeds = 96 runs.
- Grading: deterministic exec of the ORIGINAL test snapshot (adapter ruling 3, Buzz event 64cc8605) — the solution is graded against the original test file content captured at workspace setup, never a workspace copy an agent may have rewritten.
- A-completion rule (adapter ruling 2, Buzz event 64cc8605; CHANGELOG entry 1 in `HYPOTHESIS_SKELETON.md`): when A's interrupt grade is PASS, B starts from the canonical stub+test workspace. A-complete runs are counted, reported separately per task, and predeclared as analyzed as their own stratum in the confirmatory analysis.

## Selection rule
- A task enters the hard tier iff **pooled success across families is within [20%, 80%]**. Pooled success = fraction of runs where B's solution passes the original test snapshot, over all runs (A-complete runs included; reported separately).
- Target tier size: **8**. If more than 8 qualify, take the 8 closest to 50% pooled. If fewer than 6 qualify, **STOP and report for redesign**.

## Reporting
Per-task per-family success, pooled rates, selected tier (or STOP), A-completion counts, tool-metadata anomalies (unknown/hallucinated tools, malformed args, path-sanitization events), cost. Verification protocol: commit hashes, git log, ls-remote, run-log paths (`part3/calib_logs/`).

## CHANGELOG
(empty at seal)
