---
title: "Earned Revision — Decision Log"
tags: [earned-revision, decision-log, research]
status: active
created: 2026-08-02
---

# Earned Revision — Decision Log (artifact phase)

Chronological record of decisions made during the prior-art/artifact phase (authorization: Buzz event `498e17ba…`). Each entry states the decision, the evidence basis, and the path to override it.

## D-2026-08-02-1: Artifact phase was not previously completed — completing it now

**Decision:** The abstract-level novelty scan (Buzz event `78121f6d…`, 2026-08-02) was delivered, but the artifact phase (full-text reading, project directory, commit) had not been completed when Sol requested the completion report (event `9ad77c3b…`). Evidence: no project directory existed in the Nest; no commit existed in any candidate repo; the work was mid-flight in `~/.buzz/.scratch/earned-revision/` (full texts fetched, no artifacts written). **Decision:** complete the authorized work and report under the task thread; do not re-run the abstract-level scan. Override path: principal confirms the artifacts were wanted at a different location.

## D-2026-08-02-2: Repository boundary — handoff-bench, dedicated branch, dedicated directory

**Decision:** Commit the artifacts to `~/handoff-bench` (Nest symlink `~/.buzz/REPOS/handoff-bench`) on a new branch `earned-revision`, in a dedicated directory `EARNED_REVISION/`. Basis: (a) the only research-class repositories in the verified Nest structure are `handoff-bench` (active research bench: preregistrations, hypothesis skeletons, predictions) and `sameriver-site` (public site — a research brief is not public site content); (b) `handoff-bench` already follows a per-study branch/directory pattern (`part3/` on branch `part3`), which this replicates; (c) `~/calib-bench` is a completed, data-frozen study repo and is not a home for a new project brief. **Separation:** the directory and branch keep Earned Revision fully separate from the Part III handoff work — no conflation. Override path: principal directs a different repo (e.g., a future dedicated research repo).

## D-2026-08-02-3: Worktree isolation from in-flight Part III Stage 0 work

**Decision:** The main `handoff-bench` checkout is on branch `part3` with in-flight, uncommitted Stage 0 files (`part3/stage0_harness.py`, `part3/stage0_tasks.py`) owned by another workstream. To avoid any risk of sweeping those files into a commit or disturbing the checkout, the artifacts are being committed from a **separate git worktree** (`/Users/jakeprokopets/handoff-bench-earned-revision`, branch `earned-revision` from `origin/main`). Evidence: `git status` showed the untracked part3 files before this phase. Override path: none needed — the main checkout is untouched.

## D-2026-08-02-4: Binder et al. 2024 citation — resolved

**Decision:** Resolve the internal "Binder et al. 2024" reference (pred-5 preemption note, `sameriver-site/src/content/predictions/predictions.json`) to **Binder, F.J., Chua, J., Korbak, T., Sleight, H., Hughes, J., Long, R., et al., *Looking Inward: Language Models Can Learn About Themselves by Introspection*, arXiv:2410.13787, submitted 17 Oct 2024** — the only Binder et al. 2024 primary work on introspective accuracy found in the literature, and full text confirms the introspection/self-prediction content matching the internal record. Basis: arXiv record (2410 = Oct 2024), full text read, author/date/topic match. Caveat: the internal record's author is Claude; recommend a one-line confirmation from the record owner that this is the paper they intended. If they meant a different "Binder 2024," re-review is required — but no other candidate exists in the primary literature searched.

## D-2026-08-02-5: Novelty classification upheld after full-text review

**Decision:** The abstract-level classification ("new empirical test / new framing, plausibly new combination") **survives full-text review**, with the duplication threat concentrated in EVU (arXiv:2604.17252) and Failing to Falsify (arXiv:2604.02485). Basis: nine full texts read; no primary study was found testing a precommitted, content-scored, decision-relevant falsifier before evidence with belief-update, calibration, and near-miss outcomes. The classification is conditional: it depends on the falsifier's decision-relevance/content-scoring and the matched-elaboration control being load-bearing (see PROJECT_BRIEF and DESIGN_NOTES). Stop condition re-checked: not triggered.

## D-2026-08-02-6: Push withheld — local commit reported

**Decision:** Commit locally on branch `earned-revision`; **do not push**. Basis: the task authorization states "Push only if that repository's standing workflow authorizes it; otherwise report the local commit and do not invent remote permission." No explicit push authorization was given for this task; the `part3` precedent involved explicit per-task authorization and cross-agent remote verification. Absent that, the default (report local commit) applies. Override path: principal says "push" and it is a one-command, reversible action.

## D-2026-08-02-7: Full texts stored as scratch, checksums as provenance

**Decision:** Full texts live in `~/.buzz/.scratch/earned-revision/fulltext/` (disposable per Nest convention); SHA-256 checksums recorded in `PRIOR_ART.md` so sources are verifiable and re-fetchable by arXiv ID. Papers are re-fetchable from arXiv (arXiv HTML/ar5iv), so scratch disposal does not lose provenance.

## D-2026-08-02-8: Part III review archived as separate, complete deliverable

**Decision:** Archive Sol's bounded adversarial methods review of Part III (delivered as Buzz event `71f6e357…`, 2026-08-02, Projects channel) into `PART_III_METHODS_REVIEW.md`, labeled separate and complete, with provenance. It is **not** part of the Earned Revision design and must not be treated as such. Basis: task instruction 4 ("archive Sol's already-delivered bounded review; label it separate and complete").

## No-code confirmation

No experiment code, no datasets, no model runs, no merges, no deployment occurred in this phase. The only files created are the five markdown artifacts in `EARNED_REVISION/` (this one included) and a session log in the Nest `WORK_LOGS/`.
