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

2. (2026-08-02, Round-3 ruling 1 at Buzz event 1885cf44) **Interrupt moves: A at turn 4 of a nominal 8-turn budget** (previously turn 7 of 12, the V3 convention). Trigger: ruling-2 sequencing rule — Round-2 pooled A-completion was 80.6% (58/72), above the 50% threshold. Rationale: difficulty alone (Round 2) reduced A-completion only 100% → 80.6%; the earlier interrupt is the primary lever for restoring the partial-work premise. **B budget unchanged at 5 turns** to preserve V3's B-budget for descriptive anchor comparability. **Part-II comparability cost:** the A-side interrupt point differs from V3's 7/12, so A-side behavior is not directly comparable to V3; anchor tasks remain descriptive-only at the V3 convention per the methods review firewall (no hypothesis tests on anchors).
