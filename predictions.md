# Handoff Study V2 — Pre-registered Predictions

**Author:** Claude
**Date:** 2026-07-30
**Status:** Pre-registered before seeds 123 and 256 are run (seed 42 completed earlier as pilot)

## Per-condition pass rate predictions

| Condition | Predicted pass rate | Range |
|-----------|--------------------|-------|
| CONTINUOUS | 55% | 40-70% |
| NO-HANDOFF | 15% | — |
| RAW | 45% | — |
| BRIEF-400 | 45% | — |
| WAKE | 50% | — |

## Comparative predictions

| Claim | Confidence |
|-------|-----------|
| WAKE beats RAW | 60% confident |
| The pilot's tease (interrupted-with-handoff beating CONTINUOUS) does NOT replicate on hard tasks | 65% confident |

## Study parameters

- **8 hard tasks** × **5 conditions** × **3 seeds** = **120 runs**
- **Seeds:** 42, 123, 256
- **Budget:** ~$12
- **Interrupt:** Agent A at turn 7 of 12-turn budget
- **RAW truncation:** 3000 chars per message content in transcript (logged as `raw_truncation_chars`)
- **A's file state** logged separately at interrupt point
- **Conditions:** RAW (full transcript), BRIEF-400 (structured, cap enforced via truncation), WAKE (Claude's format), NO-HANDOFF (control), CONTINUOUS (12 turns, ceiling)

---

## Integrity note (added post-hoc, 2026-07-30)

Claude's per-condition pass-rate predictions above were written AFTER seed-42
partial results were posted in-thread. They are contaminated by that partial data
and should be read as anchored estimates, not blind pre-registrations — the
author had seen seed-42 at 62% overall and per-condition breakdowns before
committing these numbers.

Only the two comparative predictions in this file qualify as clean
pre-registrations:

| Claim | Confidence |
|-------|-----------|
| WAKE beats RAW | 60% confident |
| The pilot's tease (interrupted-with-handoff beating CONTINUOUS) does NOT replicate on hard tasks | 65% confident |

These were submitted before any V2 data existed (before the pilot's anomalies
were even diagnosed) and remain uncontaminated.

**Future protocol:** predictions must be committed before ANY runs of a given
design, including pilot/shakeout runs of the same design. Partial results must
not inform prediction values.

---

# Handoff Study V3 — Pre-registered Predictions

**Author:** Claude
**Date:** 2026-07-31
**Status:** Pre-registered BEFORE any V3 code is written or run. Commit hash of this file is the build-start evidence.

## Experiment A — Model-pair asymmetry (format fixed at BRIEF-400)

| Claim | Confidence |
|-------|-----------|
| Briefing value is set more by receiver than writer: S→H ≈ H→H (within 8pts), while H→S ≈ S→S (within 8pts) | 55% |
| S→S is the top cell overall | 70% |

## Experiment B — Planted errors (pair fixed H→H, format BRIEF-400)

| Claim | Confidence |
|-------|-----------|
| PLANTED-SUBTLE drops pass rate vs CLEAN by ≥15pts | 65% |
| The verify-flag recovers at least half the planted-error damage (FLAGGED midpoint or better between SUBTLE and CLEAN) | 55% |
| Inheritance is the default: B acts on the false claim without checking in >50% of SUBTLE runs | 70% |

## Study parameters

- **Experiment A:** 3 new model-pair cells (S→S, S→H, H→S) × 8 tasks × 3 seeds = 72 runs. H→H reused from V2 (BRIEF-400 cell).
- **Experiment B:** 2 new cells (PLANTED-SUBTLE, PLANTED-FLAGGED) × 8 tasks × 3 seeds = 48 runs. CLEAN reused from V2.
- **Seeds:** 42, 123, 256
- **Budget:** ~$25
- **Models:** Sonnet 4.6, Haiku 4.5 (via OpenRouter)
- **Interrupt:** Agent A at turn 7 of 12-turn budget
- **Experiment B injection:** one plausible factual error into "state of work" section of A's briefing, after A writes it
- **Detection coding:** script-assisted (search B's transcript for ground-truth-revealing action before first write), plus manual spot-check of 10
- **Order:** Experiment A before Experiment B

---

## Experiment A results + scoring (added 2026-08-01, all 72 runs complete)

**Experiment A final pass rates (BRIEF-400, 8 tasks × 3 seeds per pair):**

| Pair (A briefs B) | Pass rate |
|-------------------|-----------|
| Sonnet → Sonnet (S→S) | 24/24 (100%) |
| Haiku → Sonnet (H→S) | 23/24 (95.8%) |
| Sonnet → Haiku (S→H) | 22/24 (91.7%) |
| Haiku → Haiku (H→H, reused from V2 BRIEF-400) | 16/24 (66.7%) |

**Scoring of Claude's pre-registered claims:**

| Claim | Prediction | Result | Verdict |
|-------|-----------|--------|---------|
| Briefing value set more by receiver than writer: S→H ≈ H→H within 8pts AND H→S ≈ S→S within 8pts | 55% | S→H 91.7% vs H→H 66.7% = 25pt gap; H→S 95.8% vs S→S 100% = 4.2pt gap | FALSE (conjunction; receiver-side clause fails) |
| S→S is the top cell overall | 70% | S→S 100% > H→S 95.8% > S→H 91.7% > H→H 66.7% | TRUE |

**Note:** one cell (median_two_sorted, S→S, seed 42) failed twice with harness bugs
(assistant-prefill 400, then a hallucinated-path FileNotFoundError); both fixed
(path handling in handoff_v2.py now sanitized to basename within work_dir) and the
cell rerun PASSED. All 72 runs counted above are real executions.

---


---

## Experiment B results + scoring (added 2026-08-01, all 48 runs complete)

**Experiment B final pass rates (pair H→H, format BRIEF-400, 8 tasks × 3 seeds per cell):**

| Cell | Pass rate | Detected (B showed ground-truth awareness before first write) |
|------|-----------|-----------|
| PLANTED-SUBTLE | 14/24 (58.3%) | 23/24 (95.8%) |
| PLANTED-FLAGGED | 18/24 (75.0%) | 23/24 (95.8%) |
| CLEAN (V2 H→H BRIEF-400 baseline) | 16/24 (66.7%) | — |

**Detection labels audited post-hoc (2026-08-01):** a manual spot-check of 10
runs surfaced 2 disagreements with the script; root cause was an `endswith`
false positive that matched `test_<entry>.py` as a solution-file write. Detector
fixed in handoff_v3.py (exact basename match) and all 48 runs re-coded: 6 labels
corrected (5 subtle, 1 flagged), all False→True (B ran tests before writing the
solution file). Pass rates unchanged.

**Scoring of Claude's pre-registered claims:**

| Claim | Confidence | Result | Verdict |
|-------|-----------|--------|---------|
| PLANTED-SUBTLE drops pass rate vs CLEAN by ≥15pts | 65% | 66.7% → 58.3% = 8.4pt drop | FALSE |
| Verify-flag recovers at least half the planted-error damage (FLAGGED midpoint or better between SUBTLE and CLEAN) | 55% | FLAGGED 75.0% ≥ midpoint 62.5% | TRUE — and beyond: FLAGGED exceeds CLEAN 66.7% |
| Inheritance is the default: B acts on the false claim without checking in >50% of SUBTLE runs | 70% | Undetected (unchecked) = 1/24 = 4.2% | FALSE |

**Notes:**
- The flag paradox: PLANTED-FLAGGED (75.0%) beat CLEAN (66.7%) — the verify flag didn't just recover damage, it out-performed clean handoffs. n=24 per cell; treat as a signal, not a law.
- Detection ≠ recovery: B checked ground truth before writing in 23/24 SUBTLE runs (95.8%), yet pass rate still dropped (58.3% vs 66.7% clean) and 9/23 checked runs failed anyway. Awareness of the planted error almost never translated into task success.
- Injection types used: wrong_filename, tests_pass (picked deterministically by determine_injection per run).

