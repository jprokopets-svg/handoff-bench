# Handoff Part III — Stage 0 Report (transport feasibility)

Executed by Pi per Stage 0 authorization (Buzz event 79096ec2), protocol in `part3/STAGE0_PREREG.md` (commit 6f9078e). Self-pair transport: A and B use the same family model. CLEAN-style BRIEF-400 briefing per run, no error, no cue. Seed 42. 4 families x 5 non-study tasks = 20 runs.

**Budget: $0.1619 spent (cap $8, authorization $10).**

## Family verdicts (criterion: >=4/5 transport-complete with CONSUMED)

| Family | Model | Transport-complete | Consumption | Excluded | Verdict | Cost |
|---|---|---|---|---|---|---|
| claude | `anthropic/claude-haiku-4.5` | 5/5 | 5/5 | 0/5 | **PASS** | $0.1121 |
| gpt | `openai/gpt-5-mini` | 5/5 | 5/5 | 0/5 | **PASS** | $0.0291 |
| gemini | `google/gemini-2.5-flash` | 4/5 | 4/5 | 1/5 | **PASS** | $0.0114 |
| deepseek | `deepseek/deepseek-v3.2` | 4/5 | 4/5 | 0/5 | **PASS** | $0.0092 |

All four families PASS -> per prereg (e), the study proceeds to Stage 0 review.

## Per-run detail

### claude (`anthropic/claude-haiku-4.5`)

| Task | A pass | B pass | Consumption | First read_briefing | First solution write | Transport | Run cost |
|---|---|---|---|---|---|---|---|
| two_sum | True | True | CONSUMED | 0 | 3 | True | $0.02291 |
| valid_palindrome | True | True | CONSUMED | 0 | 3 | True | $0.02168 |
| fibonacci | True | True | CONSUMED | 0 | 3 | True | $0.02104 |
| count_bits | True | True | CONSUMED | 0 | 3 | True | $0.02179 |
| climbing_stairs | True | True | CONSUMED | 0 | 3 | True | $0.02469 |

### gpt (`openai/gpt-5-mini`)

| Task | A pass | B pass | Consumption | First read_briefing | First solution write | Transport | Run cost |
|---|---|---|---|---|---|---|---|
| two_sum | True | True | CONSUMED | 0 | 2 | True | $0.00571 |
| valid_palindrome | True | True | CONSUMED | 0 | 2 | True | $0.00581 |
| fibonacci | True | True | CONSUMED | 0 | 2 | True | $0.00616 |
| count_bits | True | True | CONSUMED | 0 | 2 | True | $0.00532 |
| climbing_stairs | True | True | CONSUMED | 0 | 2 | True | $0.00615 |

### gemini (`google/gemini-2.5-flash`)

| Task | A pass | B pass | Consumption | First read_briefing | First solution write | Transport | Run cost |
|---|---|---|---|---|---|---|---|
| two_sum | True | True | CONSUMED | 0 | 1 | True | $0.00250 |
| valid_palindrome | True | True | CONSUMED | 0 | 1 | True | $0.00229 |
| fibonacci | True | True | CONSUMED | 0 | 1 | True | $0.00227 |
| count_bits | True | True | CONSUMED | 0 | 1 | True | $0.00209 |
| climbing_stairs | — | — | EXCLUDED (api_failure: degenerate empty response (finish=stop)) | — | — | — | $0.00229 |

### deepseek (`deepseek/deepseek-v3.2`)

| Task | A pass | B pass | Consumption | First read_briefing | First solution write | Transport | Run cost |
|---|---|---|---|---|---|---|---|
| two_sum | True | True | CONSUMED | 0 | 2 | True | $0.00187 |
| valid_palindrome | True | True | CONSUMED | 0 | 3 | True | $0.00215 |
| fibonacci | True | True | CONSUMED | 0 | 4 | True | $0.00181 |
| count_bits | True | True | CONSUMED | 0 | 3 | True | $0.00152 |
| climbing_stairs | True | False | NO-SOLUTION-WRITE | 0 | None | False | $0.00184 |

## Briefing-consumption transcript evidence (tool-call order, B)

Consumption coded blind to outcome: `read_briefing` must precede first `write_file` to the solution file (prereg b).

**claude**
- two_sum: CONSUMED — B order: read_briefing, read_file, read_file, write_file, run_tests, finish
- valid_palindrome: CONSUMED — B order: read_briefing, read_file, read_file, write_file, run_tests, finish
- fibonacci: CONSUMED — B order: read_briefing, read_file, read_file, write_file, run_tests, finish
- count_bits: CONSUMED — B order: read_briefing, read_file, read_file, write_file, run_tests, finish
- climbing_stairs: CONSUMED — B order: read_briefing, read_file, read_file, write_file, run_tests, finish

**gpt**
- two_sum: CONSUMED — B order: read_briefing, read_file, write_file, run_tests, finish
- valid_palindrome: CONSUMED — B order: read_briefing, read_file, write_file, run_tests, finish
- fibonacci: CONSUMED — B order: read_briefing, read_file, write_file, run_tests, finish
- count_bits: CONSUMED — B order: read_briefing, read_file, write_file, run_tests, finish
- climbing_stairs: CONSUMED — B order: read_briefing, read_file, write_file, run_tests, finish

**gemini**
- two_sum: CONSUMED — B order: read_briefing, write_file, run_tests, finish
- valid_palindrome: CONSUMED — B order: read_briefing, write_file, run_tests, finish
- fibonacci: CONSUMED — B order: read_briefing, write_file, run_tests, finish
- count_bits: CONSUMED — B order: read_briefing, write_file, run_tests, finish
- climbing_stairs: EXCLUDED — api_failure: degenerate empty response (finish=stop)

**deepseek**
- two_sum: CONSUMED — B order: read_briefing, read_file, write_file, run_tests, finish
- valid_palindrome: CONSUMED — B order: read_briefing, read_file, read_file, write_file, run_tests
- fibonacci: CONSUMED — B order: read_briefing, read_briefing, read_file, read_file, write_file
- count_bits: CONSUMED — B order: read_briefing, read_file, read_file, write_file, run_tests
- climbing_stairs: NO-SOLUTION-WRITE — B order: read_briefing, read_briefing, read_file, read_file

## Tool-interaction metadata summary (B; the pilot's real deliverable per prereg d)

**claude**
- two_sum: calls=6 counts={'read_briefing': 1, 'read_file': 2, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- valid_palindrome: calls=6 counts={'read_briefing': 1, 'read_file': 2, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- fibonacci: calls=6 counts={'read_briefing': 1, 'read_file': 2, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- count_bits: calls=6 counts={'read_briefing': 1, 'read_file': 2, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- climbing_stairs: calls=6 counts={'read_briefing': 1, 'read_file': 2, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0

**gpt**
- two_sum: calls=5 counts={'read_briefing': 1, 'read_file': 1, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- valid_palindrome: calls=5 counts={'read_briefing': 1, 'read_file': 1, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- fibonacci: calls=5 counts={'read_briefing': 1, 'read_file': 1, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- count_bits: calls=5 counts={'read_briefing': 1, 'read_file': 1, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- climbing_stairs: calls=5 counts={'read_briefing': 1, 'read_file': 1, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0

**gemini**
- two_sum: calls=4 counts={'read_briefing': 1, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- valid_palindrome: calls=4 counts={'read_briefing': 1, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- fibonacci: calls=4 counts={'read_briefing': 1, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- count_bits: calls=4 counts={'read_briefing': 1, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- climbing_stairs: EXCLUDED

**deepseek**
- two_sum: calls=5 counts={'read_briefing': 1, 'read_file': 1, 'write_file': 1, 'run_tests': 1, 'finish': 1} unknown=[] malformed=0 path_sanitized=0
- valid_palindrome: calls=5 counts={'read_briefing': 1, 'read_file': 2, 'write_file': 1, 'run_tests': 1} unknown=[] malformed=0 path_sanitized=0
- fibonacci: calls=5 counts={'read_briefing': 2, 'read_file': 2, 'write_file': 1} unknown=[] malformed=0 path_sanitized=0
- count_bits: calls=5 counts={'read_briefing': 1, 'read_file': 2, 'write_file': 1, 'run_tests': 1} unknown=[] malformed=0 path_sanitized=0
- climbing_stairs: calls=4 counts={'read_briefing': 2, 'read_file': 2} unknown=[] malformed=0 path_sanitized=0

## Adapters / deviations (recorded for the methods review)

1. **Gemini tool protocol adapter** (prereg a, per-family): Gemini via OpenRouter intermittently emits its tool-call JSON as plain truncated content instead of structured `tool_calls` (imitation of the V2/V3 JSON-in-history convention). Fixed by switching Gemini runs to canonical OpenAI assistant-`tool_calls` + `role:tool` messages. After the adapter: 4/4 completed runs CONSUMED. One run (climbing_stairs) still hit a reproducible degenerate empty response at A turn 4 (3 attempts, same failure) -> excluded per prereg (c).

2. **B-side workspace when A completes** (transport-only adaptation): if A's grade at interrupt is PASS, B starts from the canonical stub+test workspace (A's completed solution is not inherited), so B always has a solution-write to make and the consumption ordering is testable. B's context shows B's actual file state. Without this, A-complete runs would vacuous-fail the consumption criterion (B verifies and finishes without writing).

3. **Deterministic grading**: tasks are graded by exec'ing the original test snapshot in a subprocess (rc 0 iff all asserts pass), not pytest — pytest 9.x exits 5 on module-level-assert files ('no tests ran') and agents can rewrite test files. Matches 'deterministic executable task success' and is tamper-proof.

## Notes

- deepseek/climbing_stairs: B read the briefing twice then read files, but never wrote (5-turn budget exhausted) — a genuine transport-behavior data point, not an API error; task failures are never excludable (prereg c).
- gemini/climbing_stairs: excluded (degenerate empty response, reproducible at A turn 4); gemini passes 4/5 regardless.
- No calibration, no hard-tier work, no confirmatory inference performed.
