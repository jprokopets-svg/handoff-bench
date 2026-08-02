# Handoff Part III — Hard-Tier Calibration Report

Author: Pi (execution), Claude (design review pending). Per hard-tier calibration authorization (Buzz event 64cc8605). Budget cap: $15. Scope: handoff-bench repo, part3 branch only. Prereg committed before any calibration code: `part3/CALIBRATION_PREREG.md` @ `4ffd44c`.

**OUTCOME: STOP, per prereg selection rule.** 0 of 12 candidate tasks fall in the pooled [20%, 80%] success band (fewer than 6 qualify → "STOP and report for redesign"). All 12 candidates are solved at ceiling; A-completion is 100%. Redesign recommendation in section 6.

## 1. Protocol adherence

- CLEAN BRIEF-400 briefing only, no cue, no error — selection blind to experimental condition. ✓
- Self-pair transport per family (A = B = family), matching Stage 0. ✓
- Interrupt at the V3 convention: A at turn 7 of 12, B at turn 5. ✓
- Calibration seeds 777 and 888, both outside {42, 123, 256}; burned, excluded from confirmation. ✓
- Grading: deterministic exec of the ORIGINAL test snapshot (`test_<task>.py.orig`), never a workspace copy (adapter ruling 3). ✓
- A-complete rule (adapter ruling 2; skeleton CHANGELOG entry 1): when A's interrupt grade is PASS, B starts from the canonical stub+test workspace; A-complete runs counted and reported separately. ✓
- API/schema failures excludable (prereg c); task failures never excludable. ✓

## 2. Run inventory

- 4 families × 12 candidates × 2 seeds = **96 runs**; **$0.9079 total** (cap $15; ~$0.0095/run).
- 9 excluded (all gemini, excludable API failures — see §5); **87 completed runs**.
- Resume: 8 deepseek s888 runs (interrupted in a prior session) were completed this turn; the harness resume path was corrected to cache all completed runs (previously only excluded ones), so no completed run was re-executed or overwritten and no budget double-spent. All 96 runs present in `part3/calib_logs/`.

## 3. Per-task per-family success (non-excluded runs; pooled = B passes / completed)

| task | claude | gpt | gemini | deepseek | **pooled** | n | excl |
|---|---|---|---|---|---|---|---|
| atoi_clone | 2/2 | 2/2 | 2/2 | 2/2 | **100%** | 8 | 0 |
| longest_substring_no_repeat | 2/2 | 2/2 | 2/2 | 2/2 | **100%** | 8 | 0 |
| max_area_container | 2/2 | 2/2 | 2/2 | 1/2 | **87.5%** | 8 | 0 |
| interval_merge | 2/2 | 2/2 | 2/2 | 1/2 | **87.5%** | 8 | 0 |
| rotate_image | 2/2 | 2/2 | 2/2 | 2/2 | **100%** | 8 | 0 |
| valid_bst | 2/2 | 2/2 | 1/1 | 1/2 | **85.7%** | 7 | 1 |
| lru_cache | 1/2 | 2/2 | 0/0 | 2/2 | **83.3%** | 6 | 2 |
| trie_impl | 2/2 | 2/2 | 2/2 | 1/2 | **87.5%** | 8 | 0 |
| decode_string | 2/2 | 2/2 | 0/0 | 2/2 | **100%** | 6 | 2 |
| course_schedule | 2/2 | 2/2 | 0/0 | 2/2 | **100%** | 6 | 2 |
| min_window_substring | 2/2 | 2/2 | 1/1 | 2/2 | **100%** | 7 | 1 |
| find_duplicate_number | 2/2 | 2/2 | 1/1 | 2/2 | **100%** | 7 | 1 |

Family totals (non-excluded): claude 23/24 (96%), gpt 24/24 (100%), gemini 15/15 (100%), deepseek 20/24 (83%).

## 4. Selection rule → STOP

Pooled success is ≥83.3% for every candidate; **0 tasks in [20%, 80%]**. Per `CALIBRATION_PREREG.md`: "If fewer than 6 qualify, STOP and report for redesign." No tier is selected. No confirmatory work proceeds.

### A-completion (reported separately, adapter ruling 2)

**87/87 completed runs are A-complete** (A passed at the turn-7 interrupt in every run, every family, every task). Per task: atoi 8/8, longest_substring 8/8, max_area 8/8, interval_merge 8/8, rotate 8/8, valid_bst 7/7, lru_cache 6/6, trie 8/8, decode_string 6/6, course_schedule 6/6, min_window 7/7, find_duplicate 7/7.

Because A always completes, every B ran the A-complete path: canonical stub+test workspace plus a briefing describing a working solution and passing tests. Calibration therefore measured **fresh-solve-with-hint difficulty, not handoff-of-partial-work difficulty** — the 20–80% band was premised on partial-work handoffs where A-completion is rare (as your ruling 2 anticipated).

### Why the band failed: candidates are not materially harder than V2

The V2 tier (same harness family, `data_v2/`, 118 result files) spans the intended band: n_queens **7%**, word_break 43%, regex_parser 53%, serialize_tree 53%, max_path_sum 60%, median_two_sorted 64%, merge_k_lists 73%, median_stream 87%. The 12 calibration candidates are single-algorithm LeetCode-mediums — at the *easy* end of V2, not "materially harder." All four frontier families (claude-haiku-4.5, gpt-5-mini, gemini-2.5-flash, deepseek-v3.2) solve them at ceiling given tool feedback.

## 5. Tool-metadata anomalies (prereg d)

1. **9 gemini exclusions** — `api_failure: degenerate empty response (finish=stop)`, reproduced across 3 attempts per run. Excludable per prereg c. Affected: course_schedule (both seeds), decode_string (both), lru_cache (both), find_duplicate_number s777, min_window_substring s888, valid_bst s888. Gemini completed 15/24; three tasks have gemini n=0. Same intermittent OpenRouter issue as Stage 0; the approved canonical-`tool_calls` adapter does not eliminate it for these inputs.
2. **3 claude B malformed tool-call events (json protocol)** — B emitted a double-nested `write_file` tool-call payload (name/arguments escaped into the name field); the harness treated it as an unknown tool and did not execute the call. 2 of 3 runs still passed; the third (**claude/lru_cache s777**) failed because B's final solution write was the malformed call → task failed. Model-behavior failure, **not** excludable; recorded as a genuine failure.
3. **4 deepseek B NO-SOLUTION-WRITE runs** — B read the briefing and files but never wrote a solution within 5 turns: interval_merge s777, valid_bst s777, trie_impl s777, max_area_container s888 (all b_pass=False). Genuine task failures, not excludable; same deliberate-but-slow pattern seen in Stage 0 (climbing_stairs).
4. **10 path-sanitization events** (A-side reads/writes with `/` in path) — sanitizer worked as designed; benign.
5. 0 malformed-argument calls outside the 3 claude events; 0 unknown tool names outside those events.

Consumption verdicts (completed runs): **83 CONSUMED** (transport_complete), 4 NO-SOLUTION-WRITE.

## 6. Redesign recommendation (for review; not implemented)

1. **Harder task pool.** Benchmark candidates against V2's harder half (pooled ≤60%): multi-stage, multi-file, or strict-contract implementations — e.g. a small interpreter, JSON parser with unicode escapes + error cases, regex engine with groups/backrefs, serializer/deserializer round-trip, balanced tree with rotations + invariants, concurrent structure with locking, DP with reconstruction. New calibration seeds, freshly burned outside {42, 123, 256, 777, 888}.
2. **Structural: interrupt A earlier** (e.g., turn 4 of 8) so A reliably leaves partial/imperfect work and B inherits real partial code — restores the "A-completion rare" premise and the intended handoff measurement. Re-derive the B turn budget from the new baseline.
3. **Predeclare the gemini transport risk** (~38% run-loss rate on certain inputs, reproducible): over-sampling or a bounded retry policy on degenerate-empty-response (bounded adapter effort per Stage 0 precedent) must be in the confirmatory prereg.

## 7. Verification

- Prereg commit: `4ffd44cc8b3342c3a5090df57262721367815a30` (CALIBRATION_PREREG.md + skeleton CHANGELOG entry 1) — committed before any calibration code or runs.
- Run logs: `part3/calib_logs/calib_results.json` (aggregate, n=96, budget $0.9079) + `part3/calib_logs/<family>/<task>_s{777,888}.json` (96 per-run records with full tool logs, briefings, code) + per-run workspace dirs.
- Implementation: `part3/calib_tasks.py` (12 candidates), `part3/calib_harness.py` (harness, resume-cache fix noted in §2).
- `git log -3` and `git ls-remote origin part3` in commit message of the reporting commit.
