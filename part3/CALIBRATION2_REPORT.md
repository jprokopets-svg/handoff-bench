# Handoff Part III — Round-2 Hard-Tier Calibration Report

Author: Pi (execution), Claude (design review pending). Per Round-2 authorization (Buzz event 3a021bab). Budget cap: $15. Scope: handoff-bench repo, part3 branch only. Prereg committed before any Round-2 calibration code: `part3/CALIBRATION2_PREREG.md` @ `0984ce2`.

**OUTCOME: STOP, per prereg selection rule.** Only 4 of 10 harder-class candidates fall in the pooled [20%, 80%] success band (fewer than 6 qualify → "STOP and report for redesign"). Difficulty alone did NOT fully restore the partial-work premise: pooled A-completion is 80.6% (58/72), still above the 50% ruling-2 threshold, so the interrupt MUST move in Round 3 as a logged protocol change. However, the harder pool did produce the intended measurement where it bit: 14 A-incomplete runs existed, concentrated in the in-band tasks, and B recovered real partial work in 4 of them. Details and redesign recommendation in §6.

## 1. Protocol adherence

- CLEAN BRIEF-400 briefing only, no cue, no error — selection blind to experimental condition. ✓
- Self-pair transport per family (A = B = family), matching Stage 0 and Round 1. ✓
- Interrupt at the V3 convention, UNCHANGED from Round 1 (ruling 2 — difficulty first): A at turn 7 of 12, B at turn 5. ✓
- Calibration seeds 555 and 666, both outside {42, 123, 256, 777, 888}; burned, excluded from confirmation. ✓
- Grading: deterministic exec of the ORIGINAL test snapshot, never a workspace copy (adapter ruling 3). ✓
- A-complete rule (adapter ruling 2; skeleton CHANGELOG entry 1): when A's interrupt grade is PASS, B starts from the canonical stub+test workspace; A-complete runs counted and reported separately. ✓
- Retry policy (ruling 3): up to 5 attempts per API call (`MAX_CALL_RETRIES = 4`); API/schema failures after exhaustion excludable; task failures never excludable. ✓
- Gemini side-test protocol (ruling 3): 2 Round-1 failing inputs × baseline + 2 alternative Gemini models, predeclared decision rule. ✓ (§4)

## 2. Run inventory

- 4 families × 10 candidates × 2 seeds = **80 runs**; **$2.1656 main** (cap $15).
- 8 excluded (all gemini, excludable API failures — see §5); **72 completed runs**.
- Gemini side-test: 3 models × 2 inputs = **6 runs**, **$0.2187**.
- **Total spend: $2.3843** (cap $15).
- Resume: 5 deepseek s666 runs (interrupted in a prior session) were completed this turn from the harness resume-cache; no completed run was re-executed or overwritten and no budget double-spent. All 80 runs present in `part3/calib2_logs/`.
- All 10 candidates were test-file-validated against a reference implementation (and broken implementations) before any API budget was spent (prereg, §candidate list). ✓

## 3. Per-task per-family success (non-excluded runs; pooled = B passes / completed)

| task | claude | gpt | gemini | deepseek | **pooled** | n | excl | A-complete |
|---|---|---|---|---|---|---|---|---|
| mini_brainfuck | 2/2 | 2/2 | 1/1 | 2/2 | **100%** | 7 | 1 | 7/7 |
| critical_path | 2/2 | 2/2 | 1/1 | 2/2 | **100%** | 7 | 1 | 7/7 |
| text_justification | 2/2 | 2/2 | 2/2 | 2/2 | **100%** | 8 | 0 | 8/8 |
| avl_tree | 2/2 | 2/2 | 2/2 | 2/2 | **100%** | 8 | 0 | 8/8 |
| json_parser | 2/2 | 2/2 | 0/1 | 2/2 | **85.7%** | 7 | 1 | 5/7 |
| token_bucket_limiter | 2/2 | 2/2 | 1/1 | 2/2 | **100%** | 7 | 1 | 6/7 |
| graph_serializer | 2/2 | 2/2 | 0/1 | 1/2 | **71.4%** | 7 | 1 | 6/7 |
| edit_distance_ops | 0/2 | 2/2 | 1/2 | 1/2 | **50.0%** | 8 | 0 | 4/8 |
| calculator_parser | 1/2 | 2/2 | 0/1 | 0/2 | **42.9%** | 7 | 1 | 4/7 |
| regex_matcher | 0/2 | 2/2 | 0/0 | 0/2 | **33.3%** | 6 | 2 | 3/6 |

Family totals (non-excluded): claude 15/20 (75%), gpt 20/20 (100%), gemini 8/12 (67%), deepseek 14/20 (70%).

**In band [20%, 80%]:** regex_matcher 33.3%, calculator_parser 42.9%, edit_distance_ops 50.0%, graph_serializer 71.4% — **4 of 10**.

## 4. Gemini side-test (ruling 3) — model-specificity of the degenerate-empty-response loss

Inputs: `course_schedule` s777 and `decode_string` s777 (Round-1 exclusions). Full transport loop (A 7 turns, brief, B 5 turns) per model. Logs: `part3/calib2_logs/side_test/<model>/`.

| model | course_schedule s777 | decode_string s777 | verdict |
|---|---|---|---|
| google/gemini-2.5-flash (baseline) | completed (a/b pass) | EXCLUDED — degenerate empty response (reproduced) | not reliable (1/2) |
| google/gemini-2.5-pro (alt1) | completed (a/b pass) | completed (a/b pass) | **RELIABLE (2/2)** |
| google/gemini-3-flash-preview (alt2) | completed (a/b pass) | completed (a/b pass) | RELIABLE (2/2) |

- The baseline **reproduced the failure** on 1/2 inputs (decode_string s777 — same input that failed in Round 1), confirming the flake is a real, input-sensitive checkpoint issue, not a one-off.
- Both alternatives transported reliably on 2/2, including the input that fails the baseline.
- **Predeclared decision rule fires:** google/gemini-2.5-pro becomes the **Gemini family representative for the confirmatory stage** (first reliable alternative in predeclared order) — logged as a per-family adapter decision (Stage 0 adapter ruling 1). gemini-3-flash-preview is a viable reserve.

## 5. Tool-metadata anomalies (prereg d)

1. **8 gemini exclusions** (40% of gemini runs) — `api_failure: degenerate empty response (finish=stop)`, reproducible after up to 5 attempts per call. Excludable per prereg c. Affected: regex_matcher (both seeds), graph_serializer s555, token_bucket_limiter s555, mini_brainfuck s666, json_parser s666, calculator_parser s666, critical_path s666. Consistent with the Stage 0 / Round-1 rate (~38%) on gemini-2.5-flash; the side-test (§4) establishes it is model-specific and the alt representative transports reliably.
2. **20 malformed tool-name events, all claude (json protocol, double-nested payloads)** — 15 of 40 claude run-records affected (A or B). The model emitted the tool-call JSON with name/arguments mangled into the name field; the harness recorded it as an unknown tool, consumed a turn, and did not execute the call. Concentrated on the multi-stage/strict-contract tasks (regex_matcher, edit_distance_ops, calculator_parser, critical_path, graph_serializer). Model-behavior failure, **not** excludable. Notably more frequent than Round 1 (3 claude B records) — the harder tasks' larger code payloads stress the model's JSON serialization. Effect on claude's task-level rates: **regex_matcher 0/2 is transport-induced** (B's only write attempts in both seeds were malformed payloads that never landed — the graded file is A's inherited code); **edit_distance_ops 0/2 is solution-quality** (B made a valid write in both seeds but the submitted solution failed the original test snapshot).
3. **6 NO-SOLUTION-WRITE verdicts** (5 genuine, 1 false negative):
   - Genuine (b_pass=False): claude regex_matcher s555/s666, deepseek regex_matcher s555/s666 (B read briefing + files, never wrote within 5 turns), gemini edit_distance_ops s666.
   - False negative (b_pass=True): **claude/calculator_parser s666** — B's write_file used an absolute path (`/tmp/calculator_parser.py`); the path sanitizer rewrote it into the workspace, B passed, but the consumption coder compares the PRE-sanitization path and classified NO-SOLUTION-WRITE. Transport flag affected; the science (b_pass on the original test snapshot) is unaffected. Predeclare for confirmatory: path-sanitized solution writes count as solution writes.
4. **6 path-sanitization events** (5 claude A, 1 claude B) — sanitizer worked as designed (B event is the §5.3 false negative).
5. 0 malformed-argument calls outside the claude events; 0 unknown tools from non-claude families.

Consumption verdicts (completed runs): **66 CONSUMED** (transport_complete), 6 NO-SOLUTION-WRITE (5 genuine).

## 6. Results, diagnosis, and redesign recommendation (for review; not implemented)

### A-completion accounting (ruling 2)

- **58/72 = 80.6% pooled A-complete at turn 7** — down from Round 1's 100% (87/87), but **still above the 50% ruling-2 threshold → the interrupt must move in Round 3 as a logged protocol change** (with the Part-II comparability cost acknowledged in the prereg, per your sequencing rule).
- 14 A-incomplete runs (19.4%): claude 5, deepseek 5, gemini 4, gpt 0.
- **B recovery from real partial work: 4/14 (28.6%)** — claude/calculator_parser s666, deepseek/json_parser s666, deepseek/edit_distance_ops s666, deepseek/token_bucket_limiter s666.
- Contrast that isolates the intended measurement: **B pass = 53/58 (91.4%) when A completed** (fresh-solve with briefing describing a working solution) vs **4/14 (28.6%) when B inherited genuine partial work**. The confirmatory error×cue effect can only be measured in the A-incomplete regime.
- **11 of 14 A-incomplete runs (78.6%) sit in the 4 in-band tasks** — the tasks that will enter the tier are exactly the ones that generate the partial-work premise (regex_matcher 3, edit_distance_ops 4, calculator_parser 3, graph_serializer 1).

### Why the band still failed

Difficulty helped directionally but not enough: A-completion dropped 100% → 80.6%, and the four hardest tasks landed in band. But 6 of 10 candidates remain at ceiling (≥85.7%), meaning B fresh-solves them regardless of A's state — those tasks are too easy *for B to fail*, which is what the band actually measures. The pool needs candidates in the class where B's fresh-solve rate is genuinely <80% — i.e. where the briefing+stub alone does not carry B to success — not merely harder single-file algorithms.

### Round 3 recommendation (per your sequencing rule and this diagnosis)

1. **Move the interrupt** — your rule fires (80.6% > 50%). Suggested: A at turn 4 of 8 (B at turn 5, or re-derived from baseline). Logged as a protocol change with the Part-II comparability cost acknowledged in the prereg; keep the anchor-task bridge for V3 comparability. This directly targets A-completion and is now the primary lever — difficulty alone was ruled out by Round 2.
2. **Harden the in-band survivors + add multi-file class.** Keep the 4 in-band tasks (regex_matcher, calculator_parser, edit_distance_ops, graph_serializer — they generate A-incompletion). Add candidates where B's fresh-solve fails: multi-file/stateful contracts (small interpreter with multi-statement state, concurrent structure with locking, protocol/state-machine implementation, multi-step pipeline with strict I/O contracts), benchmarked against the ≤60% reference class. Fresh burned seeds outside {42,123,256,777,888,555,666}.
3. **Predeclare the claude json-protocol payload risk** in the confirmatory prereg: ~37% of claude run-records emit at least one double-nested malformed tool call on hard tasks. Options: retry-on-malformed-payload at the call level (bounded, API-error-like), or count malformed final-writes honestly as task failures. Recommend the former, predeclared; otherwise claude's hard-tier rates will be depressed by transport noise.
4. **Gemini family representative: google/gemini-2.5-pro** for confirmatory (side-test §4; predeclared rule). Reserve: gemini-3-flash-preview.
5. **Confirmatory prereg additions already owed:** path-sanitized solution writes count as solution writes (§5.3); A-complete runs reported separately per ruling 2 (skeleton CHANGELOG entry 1).

## 7. Verification

- Prereg commit: `0984ce25caf5410647b28cb4b5376f0f3655758f` (CALIBRATION2_PREREG.md) — committed before any Round-2 calibration code or runs.
- Implementation: `part3/calib2_tasks.py` (10 candidates, test-file-validated), `part3/calib2_harness.py` (resume-cache harness, `MAX_CALL_RETRIES = 4`), `part3/calib2_gemini_sidetest.py` (side-test, predeclared decision rule).
- Run logs: `part3/calib2_logs/calib2_results.json` (aggregate, n=80, budget $2.1656) + `part3/calib2_logs/<family>/<task>_s{555,666}.json` (80 per-run records with tool summaries, briefings, code) + per-run workspace dirs + `part3/calib2_logs/side_test/` (6 records + results, $0.2187).
- Console logs: `part3/calib2_run*.log`, `part3/calib2_sidetest.log`.
- `git log -3` and `git ls-remote origin part3` in commit message of the reporting commit.
