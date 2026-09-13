# Handoff Part III — Round-3 Hard-Tier Calibration Report

Author: Pi (execution), Claude (design review pending). Per Round-3 authorization (Buzz event 1885cf44). Budget cap: $25. Scope: handoff-bench repo, part3 branch only. Prereg committed before any Round-3 calibration code: `part3/CALIBRATION3_PREREG.md` @ `dfe3846`.

**OUTCOME: TIER SELECTS — 6 tasks (4 survivors + 2 new).** Exactly 2 of the 7 new candidates fall in the pooled [20%, 80%] band (bencode_codec 62.5%, markdown_table 75.0%), so the tier is 4 survivors + 2 new = 6 — at the prereg's minimum (STOP only if the total tier were <6, i.e. <2 new). Ruling 1's interrupt move (A at turn 4 of 8) cut pooled A-completion from 80.6% (Round 2) to **59.8%**, and produced 35 A-incomplete runs; the selected tier contains 25 of them (53% of its 47 non-excluded runs), so the partial-work premise the confirmatory error×cue effect needs is present in the tier. **One honest flag for review: A-completion is still above your 50% threshold at turn 4.** Per the authorization I ran the protocol as specified and did not move the interrupt again.

## 1. Protocol adherence

- CLEAN BRIEF-400 briefing only, no cue, no error — selection blind to experimental condition. ✓
- Self-pair transport per family (A = B = family), matching Rounds 1–2 and Stage 0. ✓
- **Ruling 1 (interrupt move):** A interrupted at turn 4 of a nominal 8-turn budget; B budget unchanged at 5. ✓
- **Ruling 2 (task pool):** 4 Round-2 in-band survivors kept by ruling + 7 new B-fresh-solve-fails candidates, all test-file-validated against a reference implementation (PASS) and broken implementations (REJECTED) before spend (`.scratch/validate_calib3.py`). ✓
- **Ruling 3 (malformed-payload retry):** up to 3 retries per malformed tool call, each logged with the raw payload (`retry_events` in the run records). ✓
- **Ruling 4 (gemini representative):** `google/gemini-2.5-pro` used for all gemini runs; `gemini-3-flash-preview` remains the logged reserve. ✓
- **Ruling 5 (ledger):** items recorded in the run records; no confirmatory prereg and no power simulation written (per authorization). ✓
- Calibration seeds 313 and 515, both outside {42, 123, 256, 777, 888, 555, 666}; burned, excluded from confirmation. ✓
- Grading: deterministic exec of the ORIGINAL test snapshot, never a workspace copy. ✓
- A-complete rule (skeleton CHANGELOG entry 1): A-complete runs → B starts from canonical stub+test workspace; counted and reported separately. ✓
- API/schema retries up to 5 attempts (`MAX_CALL_RETRIES = 4`); API failures after exhaustion excludable; task failures never excludable. ✓

## 2. Run inventory

- 4 families × 11 tasks × 2 seeds = **88 runs**; **$6.7678 total** (cap $25).
- 1 excluded run (gemini, excludable API failure — §5); **87 completed runs**.
- Cost by family: gemini $4.3545, claude $1.8996, gpt $0.4026, deepseek $0.1112.
- Resume note: the Round-3 run was killed mid-session by the turn time limit (at 57/88 runs, $4.83). This session completed the remaining 31 (gemini 9, deepseek 22) through the harness resume-cache; the one gemini run that was mid-flight at the kill was re-run cleanly. No completed run was re-executed or overwritten and no budget was double-spent. All 88 runs are present in `part3/calib3_logs/`.

## 3. Per-task per-family success (non-excluded runs; pooled = B passes / completed)

| task | claude | gpt | gemini | deepseek | **pooled** | n | excl | A-complete | band |
|---|---|---|---|---|---|---|---|---|---|
| regex_matcher (S) | 0/2 | 1/2 | 0/2 | 0/2 | **12.5%** | 8 | 0 | 3/8 | kept (survivor) |
| calculator_parser (S) | 1/2 | 0/2 | 0/2 | 1/2 | **25.0%** | 8 | 0 | 2/8 | kept (survivor) |
| edit_distance_ops (S) | 0/2 | 1/2 | 0/2 | 0/2 | **12.5%** | 8 | 0 | 1/8 | kept (survivor) |
| graph_serializer (S) | 1/2 | 2/2 | 1/1 | 0/2 | **57.1%** | 7 | 1 | 5/7 | kept (survivor) |
| bencode_codec | 1/2 | 2/2 | 1/2 | 1/2 | **62.5%** | 8 | 0 | 5/8 | **SELECTED** |
| markdown_table | 2/2 | 1/2 | 1/2 | 2/2 | **75.0%** | 8 | 0 | 6/8 | **SELECTED** |
| csv_pipeline | 2/2 | 2/2 | 1/2 | 2/2 | 87.5% | 8 | 0 | 6/8 | out (>80%) |
| concurrent_bank | 2/2 | 2/2 | 2/2 | 2/2 | 100% | 8 | 0 | 8/8 | out (>80%) |
| rpn_assembler | 2/2 | 2/2 | 2/2 | 2/2 | 100% | 8 | 0 | 8/8 | out (>80%) |
| tcp_state_machine | 2/2 | 2/2 | 2/2 | 2/2 | 100% | 8 | 0 | 8/8 | out (>80%) |
| mini_interpreter | 0/2 | 1/2 | 0/2 | 0/2 | 12.5% | 8 | 0 | 0/8 | out (<20%) |

Family totals (non-excluded): gpt 16/22 (72.7%), claude 13/22 (59.1%), deepseek 12/22 (54.5%), gemini 10/21 (47.6%).

**New candidates in band [20%, 80%]: 2 of 7** — bencode_codec 62.5%, markdown_table 75.0%. (csv_pipeline 87.5% just misses the ceiling; mini_interpreter 12.5% just misses the floor; the three 100% tasks are again B-fresh-solvable at ceiling.)

## 4. Tier selection

- Survivors kept by ruling: `regex_matcher`, `calculator_parser`, `edit_distance_ops`, `graph_serializer`.
- New candidates selected by band: `bencode_codec` (62.5%), `markdown_table` (75.0%).
- **Selected hard tier (6 tasks):** regex_matcher, calculator_parser, edit_distance_ops, graph_serializer, bencode_codec, markdown_table.
- Target was 8 (4 + 4 new); only 2 new qualified, so the tier is 6 — the prereg's minimum, not a STOP (STOP requires <6 total).
- **Tier pooled B success: 19/47 = 40.4%** — comfortably inside the band as a set, spanning 12.5%–75.0%.
- **Tier A-completion: 22/47 = 46.8%**; tier A-incomplete runs: 25/47 = 53.2%. B pass conditional on A-incomplete within the tier: **5/25 = 20.0%** (vs 84.6% pooled across all A-complete runs) — the intended contrast is present in the tier itself.

## 5. A-completion accounting (ruling-2 sequencing metric)

- **Pooled A-complete at turn 4: 52/87 = 59.8%** (Round 1 100%, Round 2 80.6%). The interrupt move worked directionally, but is **still above the 50% threshold**.
- A-incomplete by family: gemini 13, deepseek 10, claude 9, gpt 3.
- A-incomplete by task: mini_interpreter 8, edit_distance_ops 7, calculator_parser 6, regex_matcher 5, bencode_codec 3, graph_serializer 2, csv_pipeline 2, markdown_table 2. The four survivors and the two new selections are exactly where A-incompletion concentrates.
- Contrast that isolates the confirmatory measurement: **B pass = 44/52 (84.6%) when A completed** (B fresh-solves with a briefing describing working code) vs **7/35 (20.0%) when B inherited genuine partial work**. Under the A-complete rule, the briefing's semantic relation to the workspace changes, so A-complete runs remain a separate stratum.
- Per-task per-family A-completion is in §3; the three 100%-pooled tasks (concurrent_bank, rpn_assembler, tcp_state_machine) are also 8/8 A-complete in every family — they are solved by A before turn 4 in all runs and never reach the partial-work regime.

## 6. Ruling 3 — Claude malformed-payload retry (bounded, predeclared)

- **33 retry events** on claude, the only emitter: 30 B-side, 3 A-side, across **10 distinct claude run-records** (45% of claude's 22 runs).
- Retries recovered the call in 2 B runs (both passed); **8 B runs exhausted 3 retries and consumed the turn as an honest unknown-tool failure** (b_pass=False in every one). `unknown_tools` totals: claude B 8, claude A 1.
- No other family emitted malformed tool *names*; gpt emitted 10 malformed-argument calls (6 A, 4 B) that parsed with a fallback (tool_summary `malformed_args`), and the turns completed.
- This confirms the Round-2 diagnosis: on the harder tasks, ~half of claude's run-records still emit large double-nested payloads for the solution write. Bounded retry helps a little; it is not a fix. Recommend carrying the adapter into confirmatory as predeclared (ruling 5 ledger) and keeping the honest-failure fallback.

## 7. Ruling 4 — Gemini representative (google/gemini-2.5-pro)

- 1 of 22 gemini runs excluded: `graph_serializer` s515 — `api_failure: HTTP 400 Provider returned error` (Google "referenced name `id` in function_response.response does not match to a display_name" — a tool-call schema rejection, not a degenerate-empty response).
- 21/22 gemini runs transported. The Round-1/2 degenerate-empty-response flake did **not** reappear under gemini-2.5-pro. Excludable per prereg c.
- Remaining gemini weakness is behavioral, not transport: 6 NO-SOLUTION-WRITE verdicts (§8) and 0/2 on three tasks.

## 8. Tool-metadata anomalies (prereg d)

1. **11 NO-SOLUTION-WRITE verdicts** (all non-excluded): gemini 8, deepseek 2, gpt 1, claude 0 — B read the briefing/files and never wrote a solution within 5 turns. All are b_pass=False; genuine task failures, not excludable.
2. **28 path-sanitization events, all claude A-side** (10 A-side records; zero B-side across all families). No gpt/gemini/deepseek path events. Sanitizer worked as designed. Per ruling 5 ledger item 1, path-sanitized writes count as solution writes in the confirmatory prereg; there were no B-side path events this round, so no NO-SOLUTION-WRITE false negative arose from sanitization.
3. **claude malformed-payload events** — §6.
4. **0 unknown tools from non-claude families**; 0 unhandled malformed arguments.

## 9. Empirical variance components (for the power simulation; no simulation run)

Per-task per-family B-pass across the two seeds (variance of the 0/1 pair; n=2 unless noted):

| tier task | claude | gpt | gemini | deepseek | pooled var. across family rates |
|---|---|---|---|---|---|
| regex_matcher | 0.0 (v=0.000) | 0.5 (v=0.250) | 0.0 (v=0.000) | 0.0 (v=0.000) | 0.0625 |
| calculator_parser | 0.5 (v=0.250) | 0.0 (v=0.000) | 0.0 (v=0.000) | 0.5 (v=0.250) | 0.0833 |
| edit_distance_ops | 0.0 (v=0.000) | 0.5 (v=0.250) | 0.0 (v=0.000) | 0.0 (v=0.000) | 0.0625 |
| graph_serializer | 0.5 (v=0.250) | 1.0 (v=0.000) | n=1 (n/a) | 0.0 (v=0.000) | 0.2292 |
| bencode_codec | 0.5 (v=0.250) | 1.0 (v=0.000) | 0.5 (v=0.250) | 0.5 (v=0.250) | 0.0625 |
| markdown_table | 1.0 (v=0.000) | 0.5 (v=0.250) | 0.5 (v=0.250) | 1.0 (v=0.000) | 0.0833 |

- **Mean within-cell across-seed variance: 0.1087** (max 0.25 — the binary ceiling for n=2).
- Pooled per-task Bernoulli variance p(1−p) over the tier: regex_matcher 0.109, calculator_parser 0.188, edit_distance_ops 0.109, graph_serializer 0.245, bencode_codec 0.234, markdown_table 0.188 — **mean 0.179**.
- Between-task spread of pooled tier rates is large (12.5%–75.0%), so task-level random effects will dominate run-level noise in the simulation; per-seed noise is near the binary maximum.
- No simulation and no confirmatory prereg were written, per authorization.

## 10. Verification

- Prereg commit: `dfe3846eaebf447e89bffadd0c4840acb4b92424` (CALIBRATION3_PREREG.md + skeleton CHANGELOG entry 2) — committed before any Round-3 calibration code or runs.
- Implementation: `part3/calib3_tasks.py` (11 tasks; 7 new, test-file-validated pre-spend), `part3/calib3_harness.py` (resume-cache harness; `TURNS_A_INTERRUPT = 4`, `TURNS_A_NOMINAL = 8`, `TURNS_B = 5`; malformed-payload retry per ruling 3; gemini rep per ruling 4).
- Run logs: `part3/calib3_logs/calib3_results.json` (aggregate, n=88, $6.7678) + `part3/calib3_logs/<family>/<task>_s{313,515}.json` (88 per-run records with tool summaries, briefings, code, retry events) + per-run workspace dirs.
- Console logs: `part3/calib3_run*.log` (runs 1–6; run 3 is the interrupted session, runs 4–6 are the resume).
- `git log -3` and `git ls-remote origin part3` in the commit message of the reporting commit.
