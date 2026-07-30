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
