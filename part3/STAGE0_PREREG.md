# Handoff Part III — Stage 0 Feasibility Protocol (Pre-registered)

Author: Claude (design), Pi (execution). Committed before any Stage 0 harness code, per Stage 0 authorization (Buzz event 79096ec2). Supplements HYPOTHESIS_SKELETON.md; supersedes nothing. Scope: handoff-bench repo, part3 branch only. Budget cap: $10.

## Purpose
Test transport, not science: can all four collective families (Claude, GPT, Gemini, DeepSeek) complete the handoff transport loop on 5 non-study tasks with verifiable briefing consumption, under a $10 budget cap? No calibration, no hard-tier work, no confirmatory inference until these results are reviewed.

## (a) Transport
All four families callable via OpenRouter with tool use:
- Claude: `anthropic/claude-haiku-4.5`
- GPT: `openai/gpt-5-mini`
- Gemini: `google/gemini-2.5-flash`
- DeepSeek: `deepseek/deepseek-v3.2`

Per-family adapters are permitted (enumerated feasibility change) and are limited to transport only: response normalization for reasoning-token models (GPT-5 family may return `content: null` with `tool_calls` present and needs max_tokens headroom so reasoning does not consume the whole budget), tool-call argument shape (dict or JSON string), and the "[Continue]" plain-text-turn pattern from the V3 harness. Adapters never change task content, briefing format, or the consumption criterion.

## (b) Briefing-consumption criterion (behavioral, blind to outcome)
- **Mechanism:** the harness writes the briefing to the receiver workspace as `briefing.txt`; the receiver is given a `read_briefing` tool, and its system prompt instructs it to read the briefing before writing solution code.
- **Exact transcript signature:** in the receiver's tool-call sequence, the first `read_briefing` call must occur at an earlier position than the first `write_file` call whose target basename equals the solution file `<task>.py`.
- **Coding:** scripted from tool names and argument paths only; the coder sees neither the briefing content nor the task outcome. Verdicts: CONSUMED / NOT-CONSUMED / NO-SOLUTION-WRITE.
- **First solution-file write** = first `write_file` with path basename exactly `<task>.py` (exact basename match; test-file writes excluded, per the V3 detection-audit lesson at commit dbf1c96).

## (c) Retry / exclusion
- Max 2 retries per run (A and B separately) for API/schema errors only: HTTP 4xx/5xx, transport timeouts, unparseable tool-call payloads, and degenerate empty responses (no content and no tool calls after normalization).
- API failures are excludable and are logged with the error class. Task failures (tests red) are NEVER excludable.

## (d) Logging
Full per-run tool-interaction metadata for both A and B: ordered tool calls (turn, tool, args, ok/error), per-tool counts, unknown/hallucinated tool names, malformed-argument calls, path-sanitization events (requested path rewritten to basename), and usage cost per call. This metadata is the pilot's real deliverable.

## (e) PASS/FAIL
- A run is **transport-complete** iff: A completes without excludable API failure; a briefing is generated; B completes without excludable API failure; the consumption verdict is CONSUMED; and B wrote the solution file at least once.
- A family **PASSES** iff ≥4 of 5 tasks are transport-complete with CONSUMED.
- The study proceeds iff all four families pass. Bounded adapter effort is permitted; if a family still fails after bounded effort, report and STOP for redesign.

## (f) Non-study tasks
Five simple tasks defined in `part3/stage0_tasks.py`, disjoint from the V2 task set (regex_parser, n_queens, median_stream, word_break, median_two_sorted, serialize_tree, max_path_sum, merge_k_lists) and from calib-bench task sets. These tasks are excluded from any future tier and will never be reused as study tasks.

## Design decisions (recorded per skeleton CHANGELOG rules)
- **Self-pair transport:** for each family, A (writer) and B (receiver) use the same family model, so the full transport loop — A works, briefing generated, B consumes — is tested end-to-end per family. Writer-family balancing is a confirmatory-prereg decision, not a Stage 0 decision.
- Seed 42 (the study's canonical seed); 4 families x 5 tasks x 1 seed = 20 runs.
- One CLEAN-style briefing per run (BRIEF-400 format, no error injection, no verification cue).
- Task pass/fail is recorded but is NOT part of the family PASS criterion (Stage 0 tests transport, not science).
- Hard budget stop at $8 spent; per-run logs under `part3/run_logs/<family>/`.

## CHANGELOG
(empty at seal)
