# Handoff Part III — Round-2 Hard-Tier Calibration (Pre-registered)

Author: Pi (execution), Claude (design review pending). Committed before any Round-2 calibration code or runs, per hard-tier Round-2 authorization (Buzz event 3a021bab). Budget cap: $15. Scope: handoff-bench repo, part3 branch only.

## Purpose
Select the hard task tier for the confirmatory 2x2 factorial, Round 2. Round 1 STOPPED per prereg (0/12 candidates in the pooled [20%, 80%] band; 87/87 A-complete). Round 2 tests whether task difficulty ALONE restores the partial-work premise, per ruling 2: the interrupt convention is UNCHANGED (A turn 7 of 12, B turn 5 — the V3/Part-II convention, preserved for protocol comparability). If Round 2 still shows pooled A-completion >50%, the interrupt moves in Round 3 as a logged protocol change.

## Candidate task list (10) — harder class, per ruling 1
Defined in `part3/calib2_tasks.py`; multi-stage / multi-file / strict-contract implementations benchmarked against V2's harder half (pooled <=60%: n_queens 7%, word_break 43%, regex_parser 53%, serialize_tree 53%, max_path_sum 60%). Disjoint from the V2 task set, the 5 Stage 0 tasks, and all 12 Round-1 candidates:

1. `mini_brainfuck` — Brainfuck interpreter: bracket validation, jumps, tape/pointer semantics (interpreter, edge-case-dense)
2. `json_parser` — strict JSON parser: full number grammar, string escapes incl. \uXXXX, strict rejection of trailing content/leading zeros/single quotes (parser, edge-case-dense)
3. `regex_matcher` — regex engine: classes with ranges/negation, greedy quantifiers with backtracking, groups + alternation, anchors, escapes (multi-stage)
4. `graph_serializer` — cycle- and shared-reference-preserving object serializer (strict contract, stateful format)
5. `avl_tree` — AVL insert/delete with rotations and height invariants (balanced tree with invariants)
6. `edit_distance_ops` — Levenshtein distance WITH operation-list reconstruction (DP with reconstruction)
7. `calculator_parser` — infix evaluator: ** right-assoc, unary minus, % semantics, strict errors (multi-stage lexer + parser)
8. `critical_path` — DAG longest-path project scheduling with critical-path reconstruction + cycle detection (DP/graph with reconstruction)
9. `text_justification` — full justification with greedy packing, left-to-right extra-space distribution, last-line rule (edge-case-dense)
10. `token_bucket_limiter` — token bucket with continuous refill, capping, no-deduction-on-deny, deterministic clock injection (stateful, strict contract)

**Test-file validation:** every candidate's test file was executed against a reference implementation (and wrong implementations) before any API budget was spent; all 10 pass with the reference and fail with broken implementations.

## Protocol
- CLEAN BRIEF-400 briefing per run only (no cue, no error); selection blind to experimental condition.
- Self-pair transport per family (A = B = family), matching Stage 0 and Round 1.
- Interrupt at the V3 convention, UNCHANGED from Round 1: A at turn 7 of 12, B at turn 5 (ruling 2 — difficulty first, protocol surgery only if Round 2 A-completion >50% pooled).
- **Calibration seeds: 555 and 666** — both outside {42, 123, 256, 777, 888}; thereby burned and excluded from confirmation.
- 4 families x 10 candidates x 2 seeds = 80 runs, + the Gemini side-test below.
- Grading: deterministic exec of the ORIGINAL test snapshot (adapter ruling 3) — solution graded against the original test file content captured at workspace setup, never a workspace copy.
- A-completion rule (adapter ruling 2; skeleton CHANGELOG entry 1): when A's interrupt grade is PASS, B starts from the canonical stub+test workspace. A-complete runs are counted and reported separately per task; pooled A-completion is the Round-2 decision metric for ruling 2.

## Retry / exclusion policy (ruling 3)
- **Up to 5 attempts per API call** for API/schema errors, including the Gemini degenerate-empty-response class (MAX_CALL_RETRIES = 4, vs 2 in Round 1).
- API/schema failures after exhausting retries remain excludable (prereg c, Round 1); **task failures are NEVER excludable**.

## Gemini side-test (ruling 3) — model-specificity of the ~38% Round-1 loss
- Inputs: 2 Round-1 failing (task, seed) combos on `google/gemini-2.5-flash`: `course_schedule` s777 and `decode_string` s777 (both failed with degenerate empty response at A).
- Models: baseline `google/gemini-2.5-flash`; alt1 `google/gemini-2.5-pro` (pro variant); alt2 `google/gemini-3-flash-preview` (newer flash variant; also in Paper B's switch matrix).
- Procedure: full transport loop (A 7 turns, brief, B 5 turns) on both inputs with each model. Logs isolated under `part3/calib2_logs/side_test/<model>/`.
- **Criterion:** an alternative "transports reliably" iff it completes the full transport loop (no excludable failure) on 2/2 inputs. The baseline is expected to reproduce the failure on >=1 input; if it does not, the failing-input set is re-selected from the remaining Round-1 exclusions and the side-test re-run (bounded effort).
- **Decision rule (predeclared):** if exactly one (or both) alternative transports reliably, it becomes the Gemini family representative for the confirmatory stage — a logged per-family adapter decision (ruling 1, Stage 0 adapter ruling 1). If NO Gemini model transports reliably, that is a feasibility finding reported before any confirmatory prereg.

## Selection rule (unchanged from Round 1)
- A task enters the hard tier iff **pooled success across families is within [20%, 80%]** (pooled = fraction of runs where B's solution passes the original test snapshot, over non-excluded runs; A-complete runs included, reported separately).
- Target tier size: **8**. If more than 8 qualify, take the 8 closest to 50% pooled. If fewer than 6 qualify, **STOP and report for redesign**.

## Reporting
Per-task per-family success, pooled rates, selected tier (or STOP), A-completion counts per task, tool-metadata anomalies, cost. Gemini side-test verdict + the predeclared adapter decision. Verification protocol: commit hashes, git log, ls-remote, run-log paths (`part3/calib2_logs/`).
