---
title: "Earned Revision — Prior Art (Full-Text Review)"
tags: [earned-revision, prior-art, full-text, research]
status: active
created: 2026-08-02
---

# Earned Revision — Prior Art, Full-Text Phase

Companion to `PROJECT_BRIEF.md`. This document records the **full-text** prior-art review conducted in the artifact phase (authorization: Buzz event `498e17ba…`). It supersedes the abstract-level scan (Buzz event `78121f6d…`) for factual claims: every work below was read from a fetched primary full text (arXiv HTML/ar5iv), except where explicitly flagged.

## Method and access

- Full texts fetched directly from arXiv HTML/ar5iv sources (see checksums below). Read: title/abstract, introduction/background, design/methods, and results/discussion for each.
- No blogs or secondary summaries used for factual claims.
- Full-text files are stored in the Nest scratch area: `~/.buzz/.scratch/earned-revision/fulltext/` (disposable copy; checksums below are the provenance record). Artifacts reference papers by arXiv ID so they are re-fetchable.

## Full-text checksums (SHA-256, as fetched 2026-08-02)

| Paper | File | SHA-256 |
|---|---|---|
| Binder et al. 2024 (introspection) | 2410.13787.txt | `cf6d6209f0952337d30394341462e88af89977ce3417f70981bd14c70fbb20aa` |
| Jhaveri et al. 2026 (Failing to Falsify) | 2604.02485.txt | `b9cb4c1a798329890a0c68bb8a6284384ace5086017af0de1540af78af46a935` |
| Wang et al. 2026 (EVU) | 2604.17252.txt | `e6646c120b39fc00aabff8414b4f403cfd4fca401b730017dbaa860f32b945e8` |
| Xu et al. 2026 (BeliefTrack) | 2605.30219.txt | `ec83a6d83a4df7fe780803a3e92f0311610fbc9a0930b6873b81717a4fa4beb3` |
| Dhanda 2026 (DeltaLogic) | 2604.02733.txt | `d8e6ed1b2d074be5e1192c93686f8ce41fce6c52b19d4b99ae552cae9797c929` |
| Huang et al. 2023 (self-correction) | 2310.01798.txt | `064afd253f0ea620bac0c19884cf2f730d3843d632a38e9d4e7d84a0ae2bb5af` |
| Kadavath et al. 2022 (P(True)) | 2207.05221.txt | `ee7555bf4543b47c3963cb82628c57a9214923c8d3960e79e9274707bab633b4` |
| Lin et al. 2022 (verbalized confidence) | 2205.14334.txt | `052e9871570c2bd192bb5b3f05dc70eee0fc8efc06dc508e7a5e3ee7ed41701e` |
| Sharma et al. 2023 (sycophancy) | 2310.13548.txt | `20aba87789a214d5a67771344750161e1ed2f5feeda9e89cf22ab896672dd22f` |

## Findings per paper and how each changed the brief

### 1. Jhaveri, GX-Chen, Sucholutsky, Choi 2026 — *Failing to Falsify* (arXiv:2604.02485, NYU)
- **Design:** adapts Wason's 2–4–6 rule-discovery study; the agent proposes triples, receives YES/NO feedback, and guesses the hidden rule. Eleven LLMs across families and scales; confirmation bias quantified as the incompatible/compatible test ratio.
- **Key results (full text):** models exhibit confirmation bias; success rates 6–78% within 45 interactions; longer-reasoning recent models (Qwen family) show less bias. Human-inspired interventions **Think-in-Opposites** (Branchini et al. 2023: test an instance "opposite" on a salient feature) and **Dual-Goal** (Gale & Ball 2006: guess the DAX rule and its MED complement) **improve rule discovery 42% → 56%** on average when prompted; distillation of the intervention behavior generalizes to the Blicket test.
- **Similarity / difference:** same cognitive core (falsification), but measured during *evidence search in an interactive game*, not *belief revision after evidence*; no pre-evidence commitment; no confidence/calibration outcomes; no near-miss evidence packets; no matched-elaboration control; interventions are general instructions, not model-authored specific falsifiers.
- **Threat to novelty:** medium — it establishes that "tell the model to falsify" helps hypothesis search, which is adjacent to (not identical with) the candidate. It does **not** test whether a *precommitted, decision-relevant, content-scored falsifier* changes later updating, calibration, or near-miss discrimination.
- **How it changed the brief:** (1) added to the duplication argument (finding 2); (2) motivated the matched-elaboration control: since general falsification prompting is already known to help *search*, the candidate must isolate the *commitment* effect on *updating*; (3) the Dual-Goal/Think-in-Opposites prompts are now listed as ablations/contrast arms in `DESIGN_NOTES.md`.

### 2. Wang, Leong, Wang, Li 2026 — *Seeing Isn't Believing* / **EVU** (arXiv:2604.17252, PolyU/Sichuan)
- **Design:** formal probing characterizes "belief inertia" — embodied agents stubbornly adhering to prior beliefs despite explicit observations. Introduces **Estimate-Verify-Update (EVU)**: the agent (1) estimates the expected outcome of its action before observing the result, (2) verifies the actual observation against the estimate through explicit reasoning (generating a "surprise signal" verification evidence), (3) updates its prior belief state to a grounded posterior. Integrated into both prompting- and training-based agent reasoning; three embodied benchmarks.
- **Key results (full text):** EVU yields consistent, substantial gains in task success across the three benchmarks and mitigates belief inertia.
- **Similarity:** the closest existing *intervention* — a pre-observation commitment ("estimate") that gates updating, and explicit textual belief states.
- **Difference:** (a) EVU's estimate is a *generic expected observation*, not a decision-relevant falsifier/stop condition; (b) environment gives verifiable feedback and objective outcomes — no authored evidence packets, no near-miss/irrelevant categories, no confidence outcomes; (c) no calibration or motivated-rationalization analysis; (d) no matched-elaboration control — EVU's gains could in principle be extra-deliberation effects, which is exactly the confound the candidate's arm B isolates.
- **Threat to novelty:** **medium — the strongest single threat.** If the mechanism is "predict before evidence," the candidate could be predict-then-verify renamed.
- **How it changed the brief:** made the falsifier's *decision-relevance and content-scoring* and the *matched-elaboration control* load-bearing (see PROJECT_BRIEF novelty classification). The brief now states explicitly what the candidate adds beyond a generic estimate: specific falsifier + stop condition + evidence packets categorized relative to it + calibration + rationalization analysis.

### 3. Xu et al. 2026 — *When Should Models Change Their Minds?* / **BeliefTrack** (arXiv:2605.30219, ZJU + HomologyAI)
- **Design:** Contextual Belief Management (CBM) — maintaining a predicted belief state aligned with formal evidence while isolating task-irrelevant noise. BeliefTrack: closed-world benchmark with two environments (Rule Discovery, Circuit Diagnosis), finite belief spaces, symbolic verifiers, exact turn-level evaluation. Failure taxonomy: **Failed Stay, Failed Update, Failed Isolation**. 135 Rule Discovery examples; frontier models evaluated (incl. GPT-5.2 per full text).
- **Key results (full text):** vanilla models exhibit severe CBM failures; explicit belief-tracking *prompts* give only limited gains; **RL with belief-state rewards reduces failure rates 70.9% on average**; representation-level steering reduces failure rates 46.1% across two tasks.
- **Similarity:** outcome vocabulary (Failed Stay ≈ under-update/over-stability; Failed Update ≈ under-update; Failed Isolation ≈ over-update on noise) is directly reusable; closed-world symbolic tasks are exactly the low-harm, independently adjudicable domain class the candidate prefers.
- **Difference:** a benchmark and training regime, not an intervention test of pre-evidence commitment; no confidence/calibration outcomes; no naturalistic evidence packets.
- **Threat to novelty:** low-moderate (methodology overlap, not intervention overlap). It strengthens the candidate by showing (a) belief management is measurable and (b) prompting alone gives limited gains — motivating the candidate's more structured intervention, while warning that simple prompts may under-deliver.
- **How it changed the brief:** adopted the CBM failure taxonomy as secondary-outcome vocabulary; adopted closed-world symbolic task environments (Rule Discovery, Circuit Diagnosis) as the preferred construct-validation domains.

### 4. Dhanda 2026 — *DeltaLogic* (arXiv:2604.02733, Amazon)
- **Design:** a benchmark-transformation protocol: each episode asks for an initial conclusion under premises P, applies a **minimal edit δ(P)**, then asks whether the previous conclusion should stay or be revised. Edit types: support insertion, defeating-fact insertion, support removal, irrelevant-fact addition. Instantiated from FOLIO and ProofWriter (100 episodes; reported subsets: 30-episode Qwen main, 20-episode near-4B extension). Metrics: initial accuracy, revision accuracy, **inertia rate**, over-flip rate, abstention.
- **Key results (full text):** on the completed subsets, stronger static reasoning does not imply better revision: Qwen3-1.7B 0.667 initial vs 0.467 revision accuracy with inertia 0.600 on change episodes; Qwen3-0.6B collapses into near-universal abstention; Qwen3-4B preserves the inertial pattern (0.650/0.450/0.600); Phi-4-mini-instruct much stronger (0.950/0.850) but with non-trivial abstention and control instability.
- **Similarity:** the nearest *paired initial→evidence→revised* structure; its edit taxonomy maps onto the candidate's evidence categories (support insertion ≈ decisive confirm; defeating-fact/support removal ≈ decisive disconfirm; irrelevant-fact addition ≈ irrelevant).
- **Difference:** a measurement benchmark, not an intervention; no pre-evidence falsifier elicitation; no confidence/calibration; logical-premise edits rather than naturalistic evidence packets.
- **Threat to novelty:** low — it supports the candidate's premise (revision discipline is distinct from static competence) rather than covering the intervention.
- **How it changed the brief:** the DeltaLogic result (competence ≠ revision discipline) is cited in the brief's rationale; its edit-type taxonomy informs the packet-category design in `DESIGN_NOTES.md`.

### 5. Huang et al. 2023 — *Cannot Self-Correct Reasoning Yet* (arXiv:2310.01798)
- **Key result (full text):** LLMs struggle to self-correct **without external feedback**; performance can even degrade after self-correction.
- **Relevance:** motivates the intervention — an externally elicited, precommitted criterion is a plausible mechanism for enabling correction, and the failure mode (self-correction degrades performance) warns that the falsifier must be tied to *evidence*, not to more self-deliberation.
- **How it changed the brief:** supports arm B (matched elaboration) as the critical control: if elaboration alone could self-correct, Huang et al. suggest it won't, so any observed effect is more likely attributable to the falsifier structure — while the matched control still rules out token-count effects.

### 6. Kadavath et al. 2022 — *Language Models (Mostly) Know What They Know* (arXiv:2207.05221)
- **Key results (full text):** larger models are well-calibrated on multiple-choice/true-false in the right format; P(True) self-evaluation works on open-ended sampling; P(IK) (knowing without proposing an answer) partially generalizes but struggles with calibration on new tasks; P(IK) rises appropriately with relevant context and hints.
- **Relevance:** the calibration-outcome toolkit (P(True), P(IK)) and the baseline finding that calibration depends on format — directly relevant to the candidate's "initial and final confidence format identical across arms" constraint.
- **How it changed the brief:** cited for the outcome definitions; the format-dependence finding is logged in `DESIGN_NOTES.md` (confidence reactivity).

### 7. Lin, Hilton, Evans 2022 — *Teaching Models to Express Their Uncertainty in Words* (arXiv:2205.14334)
- **Key results (full text):** a GPT-3 model can express calibrated verbalized confidence without logits; remains moderately calibrated under distribution shift; calibration depends on latent representations correlating with epistemic uncertainty. Introduces the CalibratedMath suite.
- **Relevance:** the primary-outcome measurement approach (verbalized confidence scored by Brier/log); CalibratedMath is a template domain for clean confidence scoring.
- **How it changed the brief:** cited for Brier/log scoring of verbalized confidence; CalibratedMath-style arithmetic/verifiable QA listed as a candidate domain.

### 8. Sharma et al. 2023 — *Towards Understanding Sycophancy in Language Models* (arXiv:2310.13548)
- **Key results (full text):** five AI assistants consistently exhibit sycophancy across four free-form tasks; human preference data show responses matching user views are more likely preferred; both humans and preference models prefer convincingly-written sycophantic responses over correct ones a non-negligible fraction of the time; optimizing against preference models sometimes sacrifices truthfulness.
- **Relevance:** the "evidential vs social updating" confound — a model might update to match the *framing* of evidence rather than its content. For the candidate, evidence packets must not read as "the user's view."
- **How it changed the brief:** added the sycophancy/social-updating control (confound 7) and the neutral-evidence-formatting rule in DESIGN_NOTES.

### 9. Binder et al. 2024 — *Looking Inward: Language Models Can Learn About Themselves by Introspection* (arXiv:2410.13787) — **internal citation resolved**
- **Citation resolved:** this is the "Binder et al. 2024" referenced in the internal pred-5 preemption record. First author Felix J. Binder; submitted 17 Oct 2024; full text acquired and read.
- **Design (full text):** introspection defined as acquiring knowledge from internal states, not training data; studied by finetuning models to predict properties of their own behavior in hypothetical scenarios. Test: model M1 predicts its own behavior; if introspective, M1 beats a different model M2 even when M2 is trained on M1's ground-truth behavior. GPT-4, GPT-4o, Llama-3 models.
- **Key results (full text):** M1 outperforms M2 in predicting itself (e.g., Llama-70B predicts itself 48.5% vs GPT-4o 31.8% cross-prediction; reciprocal pattern holds), evidence for privileged self-access; persists after intentionally modifying ground-truth behavior; but **introspection fails on more complex tasks and out-of-distribution generalization**; no self-prediction advantage for sycophantic behavior; limited generalization to other self-knowledge datasets.
- **Relevance to this project:** (a) resolves the internal preemption record — the original introspective-accuracy Study 2 was preempted by this line; (b) the candidate is **distinct**: Earned Revision tests a *pre-evidence falsifier intervention on subsequent belief revision*, not self-prediction of behavior; (c) Binder et al.'s finding that self-reports fail on complex/OOD tasks is a warning: trust measured *behavior* (revision + calibration), not stated self-knowledge.
- **How it changed the brief:** the preemption/duplication analysis now rests on the exact paper rather than an unlocated reference; the "no introspection advantage on complex tasks" finding is logged as a design warning (do not rely on model self-reports; measure behavior).

## Additional primary works surfaced from reference/citation scanning

- Halawi et al. 2024, *Approaching Human-Level Forecasting with Language Models*, arXiv:2402.18563 (Steinhardt group) — pre-outcome forecasting/commitment lineage; noted as the closest *human-side* precommitment analog in the LLM-forecasting line. (Identified via prior scan; full text not re-fetched this phase — flagged.)
- Lord, Lepper & Preston 1984, *Considering the opposite*, JPSP 47(6), DOI 10.1037/0022-3514.47.6.1231 — canonical human consider-the-opposite intervention; the direct human analog of the candidate's arm A. (Venue/DOI verified via Crossref in the prior scan; content canonical.)

## Unresolved items and limitations

- **Binder et al. 2024 — resolved** with the exact paper (arXiv:2410.13787). Recommendation: have the record owner (Claude, per pred-5 note) confirm this matches the reference they intended; if they meant a *different* Binder 2024 paper on belief updating specifically, that would need re-review. As far as the primary literature shows, this is the only Binder et al. 2024 work on introspective accuracy.
- **Full-text coverage is scoped** to the nine papers above (all required minimums covered) plus citation-scan notes; Semantic Scholar was rate-limited (HTTP 429) in the prior scan and was not relied on; no secondary sources used.
- **No full text was found testing precommitted-falsifier-before-evidence on LLM belief updating with confidence outcomes** — the negative is scoped to arXiv + Crossref and remains the open slot this project would fill.
- Stop condition checked: full texts do **not** show the exact intervention already adequately tested; the effect is separable from matched deliberation **only if** arm B is implemented as specified (it is load-bearing, not decorative).

## Bottom line for the brief

The novelty classification in `PROJECT_BRIEF.md` ("new empirical test / new framing, plausibly new combination") is **upheld by the full-text phase**, with the duplication threat concentrated in EVU (predict-then-verify) and Failing to Falsify (falsification prompting during search). Both are answered by making falsifier decision-relevance/content-scoring and the matched-elaboration control load-bearing features of the design.
