# Handoff Part III — Round-3 Hard-Tier Calibration (Pre-registered)

Author: Pi (execution), Claude (design review pending). Committed before any Round-3 calibration code or runs, per Round-3 authorization (Buzz event 1885cf44). Budget cap: $25. Scope: handoff-bench repo, part3 branch only. Includes skeleton CHANGELOG entry 2 (interrupt protocol change, ruling 1).

## Purpose
Select the hard task tier for the confirmatory 2x2 factorial, Round 3. Round 2 STOPPED per prereg (4/10 in band; A-completion 80.6% > 50%). Round 3 implements ruling 1 (interrupt moves), ruling 2 (task pool), ruling 3 (claude malformed-payload retry), ruling 4 (gemini representative swap), and logs ruling 5's confirmatory-prereg ledger items.

## Ruling 1 — Interrupt protocol change (skeleton CHANGELOG entry 2)
- **A is interrupted at turn 4 of a nominal 8-turn budget**: the A system prompt states a maximum of 8 turns (so A plans an 8-turn approach), but the harness stops and grades A at turn 4. B's budget is UNCHANGED at 5 turns (V3's B budget, preserved for descriptive anchor comparability; choice and rationale logged in CHANGELOG entry 2).
- Trigger: ruling-2 sequencing rule — Round-2 pooled A-completion was 80.6% (58/72), above the 50% threshold, so the interrupt moves as a logged protocol change.
- Part-II comparability cost: the A-side interrupt point (4 of 8) differs from V3's (7 of 12), so A-side behavior is not directly comparable to V3; anchor tasks remain **descriptive-only** at the V3 convention (methods review firewall). B-side behavior is comparable (B budget unchanged).
- This is the primary lever: difficulty alone (Round 2) reduced A-completion only 100% → 80.6%.

## Ruling 2 — Task pool (4 survivors + 7 new candidates)
- **KEPT by ruling** (in-band Round-2 survivors, definitions imported from `calib2_tasks.py`): `regex_matcher` (33.3%), `calculator_parser` (42.9%), `edit_distance_ops` (50.0%), `graph_serializer` (71.4%).
- **ADDED** (7 new candidates in the B-fresh-solve-fails class — multi-file/stateful/strict-contract; defined in `part3/calib3_tasks.py`):
  1. `mini_interpreter` — tiny imperative language interpreter: lexer+parser+executor, multi-statement state, nested blocks, if/else/while, strict error semantics
  2. `tcp_state_machine` — 21-transition TCP state machine with strict invalid-transition rejection
  3. `concurrent_bank` — thread-safe ledger with locking; atomic transfers; no negative balances; strict error contract
  4. `bencode_codec` — bencode encode/decode with strict rejection (leading zeros, truncation, trailing data, key types)
  5. `rpn_assembler` — stack-machine assembler+simulator: labels, jumps, underflow/div-zero/label errors
  6. `markdown_table` — GFM table → strict HTML: alignment, pipe escapes, HTML escaping, column-count errors
  7. `csv_pipeline` — strict RFC-4180 CSV parse → status-filter → numeric-then-lexicographic sort → re-serialize
- **Disjointness:** all 11 names verified disjoint from V2, Stage 0, Round-1 and Round-2 sets (script check in `calib3_tasks.py`).
- **Test-file validation (pre-spend):** every new candidate's test file was executed against a reference implementation (PASS) and against deliberately broken implementations (REJECTED) before any API budget was spent — see `.scratch/validate_calib3.py`, results in CALIBRATION3_REPORT.md.
- **Seeds:** **313 and 515** — both outside {42, 123, 256, 777, 888, 555, 666}; thereby burned and excluded from confirmation.

## Ruling 3 — Claude malformed-payload retry (bounded, predeclared)
- Up to **3 retries per malformed tool call** (a tool call whose name is not in the known-tool registry — the Round-1/2 claude double-nested-payload class). Each retry event is **logged with the raw payload** (`retry_events` in the run record). The retry re-requests the SAME call with the SAME message state — transport repair, never content editing. After 3 retries, if still malformed, the turn is consumed as an honest failure (unknown-tool handling as before, not excludable). Applied to all families (generic transport repair; claude is the observed emitter).
- Carried into the confirmatory prereg (ruling 5 ledger).

## Ruling 4 — Gemini family representative (effective immediately)
- `google/gemini-2.5-flash` → **`google/gemini-2.5-pro`** for ALL Round-3 runs, so the tier is selected on the model that will actually run in confirmatory (per the Round-2 side-test decision rule). `google/gemini-3-flash-preview` logged as reserve.
- Gemini transport adapters unchanged: canonical OpenAI tool-call protocol (Stage-0 adapter ruling 1), API retry policy up to 5 attempts (Round-2 ruling 3).

## Ruling 5 — Confirmatory-prereg ledger (accumulate; not implemented yet)
1. Path-sanitized solution writes count as solution writes (Round-2 §5.3 false-negative fix).
2. A-complete runs reported separately and analyzed as their own stratum (CHANGELOG entry 1).
3. Per-family adapters: Gemini canonical tool_calls; Claude malformed-payload retry (this prereg); Gemini family representative = gemini-2.5-pro.
4. Anchor tasks descriptive-only at the V3 convention (methods review firewall).

## Protocol (unchanged from Rounds 1–2 except where rulings above change it)
- CLEAN BRIEF-400 briefing per run only (no cue, no error); selection blind to experimental condition.
- Self-pair transport per family (A = B = family), matching Rounds 1–2.
- Interrupt: **A at turn 4 of nominal 8; B at turn 5** (ruling 1).
- 4 families × 11 tasks × 2 seeds (313, 515) = **88 runs**.
- Grading: deterministic exec of the ORIGINAL test snapshot (adapter ruling 3), never a workspace copy.
- A-completion rule (CHANGELOG entry 1): A-complete runs → B starts from canonical stub+test workspace; counted and reported separately per task.
- Retries: API/schema up to 5 attempts (`MAX_CALL_RETRIES = 4`); API failures after exhaustion excludable; task failures NEVER excludable. Claude malformed-payload retry up to 3 (ruling 3).
- GIL caveat (concurrent_bank): under the standard CPython GIL, short dict read-modify-writes are effectively atomic, so a missing lock may be masked by the GIL; the concurrency stress test is a best-effort discriminator and the sequential-semantics assertions are the deterministic ones. Recorded here for transparency.

## Selection rule (unchanged)
- A NEW candidate enters the hard tier iff pooled success across families is within **[20%, 80%]** (pooled = B passes / non-excluded runs; A-complete runs included, reported separately). The 4 survivors are KEPT by ruling regardless of their Round-3 pooled rate.
- Target tier size: **8** (4 survivors + 4 qualifying new candidates). If more than 4 new qualify, take the 4 closest to 50% pooled. If the total tier has **fewer than 6** tasks (i.e., fewer than 2 new candidates qualify), **STOP and report for redesign**.

## Reporting
Per-task per-family success, pooled rates, selected tier (or STOP), A-completion counts per task (ruling-2 sequencing metric), tool-metadata anomalies (incl. claude malformed-payload retry counts and the raw-payload log paths), cost. **If the tier selects, also report the empirical variance components needed for the power simulation** — per-task per-family B-pass variance across the two seeds — but run NO simulation and write NO confirmatory prereg without separate authorization. Verification protocol: commit hashes, git log, ls-remote, run-log paths (`part3/calib3_logs/`).
