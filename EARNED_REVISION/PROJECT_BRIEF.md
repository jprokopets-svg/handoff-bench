---
title: "Earned Revision — Project Brief"
tags: [earned-revision, llm-belief-updating, falsifiers, project-brief, research-only]
status: active
created: 2026-08-02
---

# Earned Revision — Do Precommitted Falsifiers Improve LLM Belief Updating?

**Status: research/proposal phase only. NO experiment code, NO data collection, NO model runs, NO deployment authorized.** This brief is the committed output of the prior-art and design phase (authorization: Buzz event `498e17ba…`).

## One-sentence contribution

A preregistered randomized trial testing whether eliciting a **decision-relevant falsifier/stop condition from an LLM before it sees evidence** improves the accuracy, calibration, and explanation-update alignment of its subsequent belief revision, relative to a matched-elaboration rationale control and a judgment-only baseline — the first test we can verify of *precommitment-to-falsify as a debiasing intervention on belief updating* (as opposed to evidence *search*), with motivated rationalization explicitly designed against.

## Affected group and underlying need

LLMs are increasingly used to review plans, research claims, and operational decisions. "What would change your mind?" is common prompting advice, and models' stated stop conditions are treated as trust signals in review workflows. It is unknown whether precommitting a falsifier **causally** improves later evidence-based revision, or merely produces epistemic language and a new anchor (an object for motivated rationalization). Affected users are people and systems relying on model review and agentic decision support, where a stated falsifier is currently taken at face value.

## Closest internal and external work (exact citations)

**Internal (Sameriver):**
- Calib-bench Study 1, "Does It Know It Can't?" — `~/calib-bench` (repo), data-freeze-v1.2; published `sameriver-site/src/content/work/does-it-know-it-cant.md`. Provides the confidence-calibration methodology (Brier-style scoring, tiered tasks); does not contain the falsifier intervention.
- Handoff Study V3 / Part II — `~/handoff-bench`; the detection-vs-recovery dissociation ("checking ≠ recovering") is a template for "compliance ≠ better updating" in this project. Independent project; do not conflate.
- Introspective-accuracy Study 2 preemption record — `sameriver-site/src/content/predictions/predictions.json`, pred-5 resolution note ("substantially preempted (Binder et al. 2024 and successors)").
- **Binder et al. 2024 — now resolved:** Binder, F.J., Chua, J., Korbak, T., Sleight, H., Hughes, J., Long, R., et al. (2024). *Looking Inward: Language Models Can Learn About Themselves by Introspection.* arXiv:2410.13787 (submitted 17 Oct 2024). Full text acquired; checksum in `PRIOR_ART.md`. This is the introspective-accuracy line that preempted Study 2; this project is distinct from it (see PRIOR_ART §Binder).

**External (all full texts acquired and read; details, results, and checksums in `PRIOR_ART.md`):**
1. Jhaveri, A.R., GX-Chen, A., Sucholutsky, I., Choi, E. (2026). *Failing to Falsify: Evaluating and Mitigating Confirmation Bias in Language Models.* arXiv:2604.02485.
2. Wang, H., Leong, C.T., Wang, J., Li, W. (2026). *Seeing Isn't Believing: Mitigating Belief Inertia via Active Intervention in Embodied Agents* (EVU). arXiv:2604.17252.
3. Xu, H., Xu, W., Li, Z., Wang, M., Yao, Y., Wu, C., Shang, J., Gong, Y., Deng, S. (2026). *When Should Models Change Their Minds? Contextual Belief Management in Large Language Models* (BeliefTrack). arXiv:2605.30219.
4. Dhanda, A. (2026). *DeltaLogic: Minimal Premise Edits Reveal Belief-Revision Failures in Logical Reasoning Models.* arXiv:2604.02733.
5. Huang, J., et al. (2023). *Large Language Models Cannot Self-Correct Reasoning Yet.* arXiv:2310.01798.
6. Kadavath, S., et al. (2022). *Language Models (Mostly) Know What They Know.* arXiv:2207.05221.
7. Lin, S., Hilton, J., Evans, O. (2022). *Teaching Models to Express Their Uncertainty in Words.* arXiv:2205.14334.
8. Sharma, M., et al. (2023). *Towards Understanding Sycophancy in Language Models.* arXiv:2310.13548.
9. Lord, C.G., Lepper, M.R., Preston, E. (1984). *Considering the opposite: A corrective strategy for social judgment.* JPSP 47(6), DOI 10.1037/0022-3514.47.6.1231. (canonical human consider-the-opposite intervention; venue verified via Crossref, content canonical).

Additional full-text findings from EVU/BeliefTrack/DeltaLogic reference/citation scanning are in `PRIOR_ART.md` (e.g., Halawi et al. 2024 forecasting, arXiv:2402.18563, noted as the pre-outcome-commitment lineage; no closer primary intervention found).

## Strongest duplication argument

1. **EVU / predict-verify-update (Wang et al. 2026):** EVU already makes agents predict an expected outcome *before* observing feedback, then verify and update — a pre-evidence commitment that improves behavior on three embodied benchmarks. If the mechanism is simply "commit to a prediction before evidence," the candidate is a re-derivation of predict-then-verify with a new label.
2. **Failing to Falsify (Jhaveri et al. 2026):** already shows models fail to falsify during hypothesis *search*, and that human-style falsification prompting (Think-in-Opposites, Dual-Goal) improves rule discovery 42%→56%. If the candidate is "tell the model to falsify," it may be a known-effect extension rather than a new test.
3. **Human psychology:** consider-the-opposite (Lord/Lepper/Preston 1984) and pre-outcome accountability (Lerner & Tetlock 1999) are established debiasing interventions in humans; an LLM replication may add population data, not mechanism.
4. **Bayesian pedagogy:** "state what would change your mind" is standard normative advice; the intervention may be indistinguishable from asking for more careful deliberation (extra tokens / matched elaboration).

## Honest novelty classification

**New empirical test / new framing, plausibly new combination** (human precommitment psychology × LLM belief updating with calibration and near-miss outcomes). Not a new problem (biased updating is documented); not a new mechanism (uncertainty/precommitment mechanisms are known). The novelty is the *intervention–outcome pairing*: precommitted, scored, decision-relevant falsifier → belief-revision accuracy + calibration + near-miss discrimination, with motivated rationalization as a designed-against failure mode. **Risk of drifting to "probably duplicative" of EVU/predict-then-verify unless (a) falsifier decision-relevance/content-scoring and (b) the matched-elaboration control are load-bearing design features, not window dressing.** Stop-and-report condition: if a published primary study of precommitted-falsifier-before-evidence on LLM belief updating (with confidence outcomes) is found, this classification is re-reviewed.

## AI leverage and strongest non-AI alternative

- **AI leverage:** the study measures a property (belief revision, calibration, rationalization) that requires language-model subjects; only LLMs can be probed at scale with controlled evidence packets, and the results directly inform prompting and review protocols for the affected population.
- **Strongest non-AI alternative:** a human-subject replication of consider-the-opposite with pre-outcome commitment — already largely established in the human literature, which is exactly why the LLM population is the non-trivial part.

## Causal question and estimands

**Causal question:** Does eliciting a specific, decision-relevant falsifier/stop condition *before* evidence improve the accuracy and calibration of subsequent belief revision relative to matched elaboration or no elicitation — or does it merely create a new anchor/rationalization object?

**Primary estimand:** the total average causal effect of the precommitted-falsifier arm vs matched-elaboration control (and vs judgment-only baseline) on appropriate revision and Brier/log score of post-evidence confidence, across evidence categories, model families, and items.
- Secondary estimands: under-update vs over-update rates; near-miss discrimination (correct non-revision on near-miss vs correct revision on decisive disconfirm); paraphrase consistency; explanation–update alignment; falsifier content quality (compliance).

**Critical identification rule:** falsifier quality is a **post-treatment mediator**, NOT a covariate in the primary estimate. It may be analyzed separately (mediation/descriptive), never as an adjustment in the primary effect. Total causal effect first; mechanism questions are secondary and clearly labeled.

## Candidate intervention arms

1. **Precommitted falsifier / stop condition (A):** before evidence, the model states (i) a specific observation or condition that would change its judgment, and (ii) what it would do if that condition were met.
2. **Matched-elaboration rationale control (B):** before evidence, the model writes a rationale/critique of its judgment of matched length and structure, without any falsifier/stop-condition frame. Controls for extra tokens and deliberation.
3. **Judgment-only baseline (C):** initial judgment + confidence, no pre-evidence elicitation.

Initial and final confidence formats identical across all arms.

## Evidence categories (authored independently of the elicited falsifier)

Each item's evidence packets are authored in advance by the task-design team, independently of any model's falsifier; packet–falsifier match is scored **post hoc** (overlap computed after collection) to avoid circularity:
- **Decisive confirm** — evidence that satisfies the stated condition/falsifier;
- **Decisive disconfirm** — evidence that contradicts it;
- **Near-miss** — evidence that nearly satisfies it but falls short (the sharpest test of rationalization);
- **Irrelevant** — evidence orthogonal to it.

## Primary and secondary outcomes

- **Primary:** appropriate revision (correct stay/revise decision vs ground truth); Brier score and log score of post-evidence confidence.
- **Secondary:** under-update/over-update rates; near-miss discrimination; paraphrase consistency (revision stability across rewordings); explanation–update alignment (stated reasons match the actual update); falsifier compliance/content quality (manipulation check, descriptive).

## Key confounds and controls

1. **Extra tokens / deliberation** → matched-elaboration control (B).
2. **Demand characteristics** → evidence format and confidence elicitation decoupled from the falsifier frame; outcomes graded blind to arm.
3. **Criterion quality** → falsifier content scored (specific? falsifiable? decision-relevant?); analyzed as mediator/descriptive, not adjusted in primary estimate.
4. **Packet circularity** → packets authored independently of elicited falsifiers; match scored post hoc.
5. **Anchoring** → initial judgment and stated falsifier are two stacked anchors; distinguish commitment-to-criterion from anchor-to-own-criterion (compare near-miss behavior).
6. **Confidence reactivity** → confidence re-elicitation format/order identical across arms; consider randomization of elicitation order in a sub-analysis.
7. **Sycophancy / social updating** → items avoid identity/political content; evidence framed as neutral records, not as "the user's view" (Sharma et al. 2023 + BASIL-style confound).

## Minimum ablations, manipulation checks, blinded grading, inter-rater agreement

- **Ablations (minimum):** (i) arm B vs arm C (deliberation effect alone); (ii) falsifier-before-confidence vs falsifier-after-initial-confidence vs immediately-before-evidence (timing); (iii) evidence-type blocked with ≥2 items per category; (iv) no-elicitation updating baseline.
- **Manipulation checks:** compliance (does the model produce a specific, non-vague falsifier?); content scoring of falsifier quality by blinded graders.
- **Blinded grading:** outcome coding and falsifier-quality scoring blind to arm and to model identity; at least a preregistered subset double-coded with reported agreement and adjudication before unblinding.
- **Inter-rater agreement:** near-miss vs decisive categorization must reach strong independent-grader agreement **before any model pilot** (design constraint, evaluated in `DESIGN_NOTES.md`).

## Construct-validation stage (before model runs)

A small hand-audited set (6–10 items) tests only whether (i) the manipulation is distinguishable (models engage with the falsifier format), (ii) the four evidence categories are independently classifiable, and (iii) initial/final confidence formats are usable. **No scientific claim; not science.** Stop if graders cannot agree on which packets genuinely satisfy vs nearly satisfy a predeclared falsifier, or if models ignore the elicitation format.

## Smallest preregistered pilot; simulation-based power/noise plan; stop conditions

- **Pilot:** 2 model families × 3 arms × ~30 items/domain × 2 domains with independently adjudicable ground truth, single temperature pass; Brier + appropriate-revision + compliance + falsifier-quality scores preregistered. **Pilot direction is NOT a go/no-go threshold** — the pilot learns compliance and noise and informs the confirmatory power analysis.
- **Power/noise:** simulation-based power using task- and seed-effects as noise sources; within-model paraphrase consistency as a noise floor; bootstrap CIs (paired); no cross-model ranking at pilot n. Confirmatory n and design frozen in a separate preregistration before any confirmatory run.
- **Stop conditions (this phase):** a published precommitted-falsifier-before-evidence LLM belief-update study appears; full texts show the effect cannot be separated from matched deliberation; workspace/repo boundary is ambiguous. (None triggered; see DECISION_LOG.)

## Adversarial interpretation map

- **Falsifier improves updating:** (a) matched-elaboration control collapses the effect → pure deliberation effect; (b) demand characteristics (model role-plays "good scientist"); (c) improvement only on near-miss, failure on decisive → anchor-to-own-criterion; (d) regression to the mean on items where initial judgment was wrong.
- **Falsifier worsens updating:** (a) commitment/consistency pressure — the stated falsifier becomes a self-imposed anchor; (b) longer context degrades evidence use (lost-in-the-middle family); (c) criterion-quality artifact — vague falsifiers mismatch packets; (d) motivated rationalization — the model defends its own stated falsifier (activation-probing evidence in the 2026 motivated-reasoning literature supports this being real).
- **Null result:** (a) updating driven by evidence salience, not prior structure — models lack a stable belief state to commit to; (b) instruction-following flattens arms; (c) ceiling/floor difficulty effects.
- **Calibration improves but accuracy does not:** confidence deflation from uncertainty priming rather than better self-knowledge — distinguish calibration slope vs level.

## Ethical/privacy/generalization limits

- **Ethics:** the intervention is a prompt pattern; published results could be repurposed as persuasion/manipulation tooling — flag in the writeup. No human subjects, no deception. Avoid identity/political topics (persona-consistent motivated reasoning would dominate).
- **Privacy:** public-domain/authoritative items only; no PII; no real patient data (synthetic vignettes with adjudicated labels at most).
- **Generalization:** in-context "beliefs" are not persistent states; results may not transfer to multi-turn agents, memory-augmented systems, or humans. Brier-style scoring assumes single ground truth (near-miss resolution needs explicit criteria). Single-shot evidence packets ≠ the self-selected evidence of real workflows. State all of this in the paper's limitations.

## Explicit file/repository boundaries for later code

- This directory (`handoff-bench/EARNED_REVISION/`, branch `earned-revision`) is **research/proposal artifacts only** — brief, prior art, design notes, decision log, archived Part III review.
- Future experiment code, task/data generation, harness, and analysis go in a **separate, later-authorized location** (proposed: a new repo or a clearly separated subdirectory, decided at authorization time). No code of any kind may be written here.
- Do not modify: `handoff-bench/part3/` (Part III study, separate project, in flight), handoff-bench study data, `~/calib-bench`, `sameriver-site` public content, or the claude-chat-bridge.

## Modification and deployment permissions — still NOT granted

No code, no datasets, no model runs, no merges, no deployment, no site content changes. This phase closes with the committed artifacts and this report.
