---
title: "Earned Revision — Design Notes (Constraints Evaluated)"
tags: [earned-revision, design-notes, research]
status: active
created: 2026-08-02
---

# Earned Revision — Design Notes

Companion to `PROJECT_BRIEF.md`. The brief's design constraints were evaluated, not blindly accepted. This file records the evaluation and any adjustments. Every constraint below is addressed; disagreements are flagged with a decision and rationale.

## D1. Low-harm, independently adjudicable domains (evaluate)

**Constraint:** prefer synthetic rule/circuit diagnosis and verifiable numerical/factual items; avoid identity/political topics and real patient data.

**Assessment:** **accepted, with a nuance.** Full-text review strengthens this: BeliefTrack (arXiv:2605.30219) already provides exactly this class (Rule Discovery + Circuit Diagnosis with symbolic verifiers), and DeltaLogic (arXiv:2604.02733) shows logical-premise edits are cleanly adjudicable; Persona-Assigned LLMs work (arXiv:2506.20020, prior scan) shows identity content invites persona-consistent motivated reasoning that would dominate the measurement. **Adjustment:** domains should include (a) closed-world symbolic tasks (rule/circuit diagnosis) where ground truth is machine-checkable, and (b) verifiable numerical/factual items (population/date/measure figures) with authoritative ground truth. Synthetic clinical triage vignettes are acceptable only with adjudicated labels and no real patient data; they are optional, not required. Identity/political topics are excluded categorically.

## D2. Evidence packets authored independently of the elicited falsifier; match scored post hoc (evaluate)

**Constraint:** packets must be authored independently of the elicited falsifier; packet–falsifier match scored post hoc to avoid circularity.

**Assessment:** **accepted, but the design must go further than "post hoc scoring."** The circularity risk has two parts: (a) if packets are *built from* a stated falsifier, success is partly criterion quality (the brief's confound 4); (b) if match is scored by the same model that committed, scoring is self-serving. **Adjustments:**
- Packets are authored by the task-design team in advance, per item, on the basis of the item's ground truth alone (e.g., "evidence of strength X regarding claim Y"), so their decisive/near-miss/irrelevant categories exist independent of any model's falsifier.
- The *post hoc match* (packet category relative to the model's stated falsifier) is computed by **independent human graders** using a preregistered rubric (and, optionally, a second model family as a cross-check), blind to arm and to outcome.
- Near-miss vs decisive classification must reach **strong inter-grader agreement before any model pilot** (see D4). Without that, the near-miss cell is uninterpretable and the rationalization hypothesis untestable.

## D3. Initial and final confidence format identical across all arms (accept)

**Constraint:** identical confidence format across arms.

**Assessment:** **accepted.** Kadavath et al. (arXiv:2207.05221) show calibration is format-sensitive; Lin et al. (arXiv:2205.14334) show verbalized confidence can be calibrated. The constraint is necessary but not sufficient: the *elicitation order* relative to the falsifier also matters (falsifier before confidence vs after), which is why the brief includes a timing ablation. A secondary consideration: confidence elicitation is itself reactive (confidence reactivity confound), so the brief keeps confidence format/order identical and randomizes elicitation order in a sub-analysis rather than in a separate arm at pilot n.

## D4. Near-miss vs decisive evidence requires strong independent-grader agreement before any model pilot (accept, sharpen)

**Constraint:** strong agreement before any pilot.

**Assessment:** **accepted, with a sharper gate.** This is the single most important quality gate in the design: the near-miss category is the sharpest discriminator of motivated rationalization, so a mushy near-miss set would make the study's headline contrast uninterpretable. **Decision:** agreement is required on (i) packet category *intrinsic to the item* (decisive/near-miss/irrelevant relative to the item's ground truth), and (ii) the post-hoc packet–falsifier match rubric. The gate is a minimum Cohen's kappa / Krippendorff alpha specified at preregistration (not invented now); below the threshold, the item set is revised, not analyzed. This gate applies before *any* model pilot, per the constraint.

## D5. Small 6–10 item set is construct validation only, not science (accept)

**Assessment:** **accepted verbatim.** The 6–10 item hand-audited set tests manipulation distinguishability, category classifiability, and format usability only. No statistical claims. The pilot (larger, ~30 items/domain × 2 domains) is separate and also non-confirmatory. The brief says this explicitly; nothing in the artifact phase changes it.

## D6. Pilot direction must not be a go/no-go threshold; pilot informs compliance/noise and confirmatory power (accept)

**Assessment:** **accepted.** Using pilot effect direction as a gate selects on noise (a point the Part III methods review — archived in `PART_III_METHODS_REVIEW.md` — also makes for the handoff study; the same discipline applies here). **Adjustment:** the pilot has two *predeclared* pass/fail criteria that are not directional: (i) falsifier compliance (specific, non-vague, decision-relevant falsifiers produced at a predeclared rate, e.g., ≥80%), and (ii) noise estimation utility (variance components estimable at pilot n). The pilot's output feeds the simulation-based power analysis for the confirmatory preregistration. Stop conditions are listed in `PROJECT_BRIEF.md` and are not effect-direction gates.

## D7. Evidence categories: decisive confirm / decisive disconfirm / near-miss / irrelevant (accept, with mapping)

**Assessment:** **accepted.** DeltaLogic's edit taxonomy (support insertion / defeating-fact insertion / support removal / irrelevant-fact addition — arXiv:2604.02733) provides a natural, principled mapping for the closed-world task class:
- decisive confirm ≈ support insertion;
- decisive disconfirm ≈ defeating-fact insertion / support removal;
- irrelevant ≈ irrelevant-fact addition;
- near-miss ≈ a *failing* version of the support/defeating edit (an edit that nearly changes the conclusion but does not) — this category has no direct DeltaLogic equivalent and must be authored and graded with the D4 gate.

**Decision:** at least 2 items per (category × domain) cell for pilot-level block structure; the near-miss cell gets the strongest grading scrutiny.

## D8. Falsifier quality is a post-treatment mediator, not an adjustment in the primary estimate (accept)

**Assessment:** **accepted.** This is a hard identification rule in the brief: falsifier content quality is elicited *by* the treatment, so adjusting for it in the primary estimate would bias the total causal effect estimate. Quality is scored descriptively and, if a mediation analysis is ever run, it is clearly labeled secondary. This mirrors the standard guidance that post-treatment mediators are not covariates; it also matches the brief's "total causal effect as primary."

## D9. Arms: precommitted falsifier/stop condition, matched-elaboration rationale control, judgment-only baseline (accept, with control discipline)

**Assessment:** **accepted**, with three discipline notes:
1. The matched-elaboration control must be matched on *length, structure, and effort* (not just length), otherwise it is a weak control. A "critique of my judgment" of comparable token count is the operationalization; a *no-content filler* would be too weak.
2. The falsifier arm must require a **specific, decision-relevant, testable** condition and a stop action ("if X is observed, I will revise to Y"), not a generic "I might be wrong" — the compliance rubric (D6) scores this.
3. Failing to Falsify (arXiv:2604.02485) shows *general* falsification prompting helps evidence *search*; the candidate's arm A differs by (a) pre-commitment, (b) content scoring, (c) measuring belief *updating* outcomes. The Dual-Goal/Think-in-Opposites prompts are noted as optional contrast arms for a later ablation, not part of the minimum design.

## D10. Confound controls (evaluate)

**Constraint list:** extra tokens, demand characteristics, criterion quality, packet circularity, anchoring, confidence reactivity.

**Assessment:** **accepted with adjustments:**
- *Extra tokens:* arm B control (D9).
- *Demand characteristics:* outcomes coded blind to arm; evidence format decoupled from falsifier framing (D2); never tell the model the study's hypothesis.
- *Criterion quality:* scored by blinded graders; mediator, not covariate (D8).
- *Packet circularity:* D2 design.
- *Anchoring:* initial judgment and stated falsifier are two stacked anchors. The near-miss cell discriminates commitment-to-criterion (correctly standing firm on a genuine near-miss) from anchor-to-own-criterion (failing to revise on decisive disconfirm). The brief's adversarial map covers both directions.
- *Confidence reactivity:* identical format across arms (D3); order randomized in sub-analysis.

## D11. Minimum ablations, manipulation checks, blinded grading, inter-rater agreement (accept)

**Assessment:** **accepted** per brief §"Minimum ablations…". One addition: the **timing ablation** (falsifier before initial confidence / after initial confidence / immediately before evidence) is a minimum for the anchor argument, because it separates commitment-from-confidence from commitment-from-evidence-proximity. Kept in the brief.

## D12. Construct-validation stage before model runs (accept)

**Assessment:** **accepted.** The 6–10 item construct set (D5) must pass the D4 agreement gate before any model run. This is a hard ordering constraint: no model pilot before the category gate.

## D13. Smallest preregistered pilot + simulation-based power/noise + stop conditions (accept)

**Assessment:** **accepted** per brief. The pilot learns compliance and noise (D6); power is simulation-based using task/seed effects; no cross-model ranking at pilot n. Stop conditions are non-directional and listed in the brief.

## D14. Interpretation map (accept)

**Assessment:** **accepted** per brief §"Adversarial interpretation map." One addition from full-text reading: if the falsifier arm improves updating only on *decisive disconfirm* but not near-miss, that is consistent with the falsifier acting as an *attention/evidence-weighting* cue rather than a commitment device — worth pre-registering as a sub-contrast so the interpretation is not post hoc.

## Open design questions to resolve at confirmatory preregistration (not this phase)

1. Exact inter-rater agreement threshold (kappa/alpha) for D4 — to be fixed in the preregistration, informed by the construct-validation grading.
2. Exact falsifier compliance threshold and rubric wording.
3. Confirmatory sample size — from the pilot-informed simulation (not fixed now).
4. Whether a second model family is included in post-hoc packet-match scoring (cross-check).
5. Domain finalization between closed-world symbolic tasks and numerical/factual items — to be decided with the principal at authorization time, not now.

These are deliberately left open: fixing them now would be pre-analysis before any data, which this phase is not authorized to do.
