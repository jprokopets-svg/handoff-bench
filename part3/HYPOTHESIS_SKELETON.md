# Handoff Part III — Sealed Hypothesis Skeleton
Author: Claude. Committed before any Stage 0 code, per methods review (Sol, Buzz event 71f6e357). Only enumerated feasibility-driven changes permitted; all changes logged in CHANGELOG section below.

## Design frame
2×2 factorial on H-tier receivers: briefing correctness (correct / planted-error) × verification cue (none / generic cue), plus the V3 three-condition contrast (CLEAN / SUBTLE / FLAGGED) as direct replication. Cross-family: Claude, GPT, Gemini, DeepSeek families as receivers; writer family per balanced design TBD at confirmatory prereg. Primary outcome: deterministic executable task success. Secondary: verification attempt (blind-coded), detection, recovery-conditional-on-detection, overcorrection, cost.

## Sealed directional hypotheses (confidence to be finalized at confirmatory prereg; directions sealed now)
H1 (replication): planted-error+cue outperforms planted-error+no-cue on recovery, in each family.
H2 (interaction/mechanism): the cue's benefit is larger under planted-error than under correct briefings (cue × correctness interaction > 0).
H3 (cost side): under correct briefings, the cue does not improve success and may impose an overcorrection/cost penalty.
H4 (generalization): the Part II qualitative pattern (verification cue helps rather than harms) holds in at least 3 of 4 families.
H5 (family variation): effect magnitudes differ by family; no sealed direction on which family is most cue-sensitive.

## Explicitly NOT claimed
New handoff problem; generic sender×receiver pair asymmetry; belief/automation-bias language; any R2 pair-interaction estimand (deferred).

## Permitted feasibility changes (enumerated)
Task-tier composition after blind calibration; per-family API/tool-schema adaptations; retry caps; run counts after power simulation; cue exact wording after length-matching check. Nothing else.

## CHANGELOG
1. (2026-08-02, ruling at Buzz event 64cc8605) **B-workspace-when-A-completes** (science-relevant rule, from Stage 0): when A's interrupt grade is PASS, B starts from the canonical stub+test workspace — A's completed solution is not inherited — so the consumption ordering is always testable. A-complete runs are counted, reported separately, and predeclared as analyzed as their own stratum in the confirmatory analysis. Related ruling, same event: solutions are graded against the ORIGINAL test snapshot, never a workspace copy an agent may have rewritten.
