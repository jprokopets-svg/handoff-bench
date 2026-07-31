# Handoff Study V3 — Writeup Notes

For-the-record caveats logged per Claude's GO message (2026-07-31T18:13:38+00:00),
event c48160657d1a3a47c5fc1711bf2f6ff0b4a2314cefeb5b30a02fbcbfa96b1007.

## (a) Ceiling compression on Sonnet-containing cells

Experiment A pass rates: H→S 23/24 (95.8%), S→H 22/24 (91.7%), S→S 24/24 (100%),
H→H 16/24 (66.7%, reused from V2).

Sonnet-containing cells sit at 92–100%. Differences among them are unresolvable
at this n — the safe claim is "one strong participant rescues the handoff,"
not any finer ordering. 24/24 and 23/24 differ by one run; treat any ordering
of the Sonnet-containing cells as noise.

## (b) Receiver-dominance prediction scored FALSE

Claude's pre-registered claim — "briefing value is set more by receiver than
writer: S→H ≈ H→H (within 8pts), H→S ≈ S→S (within 8pts)" — scored FALSE
(confidence was 55). S→H 91.7% vs H→H 66.7% is a 25pt gap; the receiver-side
clause fails for Haiku. The writer-side clause (H→S 95.8% vs S→S 100%, 4.2pt)
holds. Keep this scored as FALSE; it goes in the writeup.

## (c) Harness bugs found mid-A and their fixes

- **Assistant-prefill 400**: `median_two_sorted`, S→S, seed 42 — the
  conversation ended on an assistant message; Anthropic rejects that. Fixed
  in commit c9871cf.
- **Path sanitization (hallucinated file path FileNotFoundError)**: same cell
  failed a second time when B wrote to a nonexistent path. Fixed in
  handoff_v2.py path handling; committed with A completion (9f2638e).
- Rerun of the cell PASSED after both fixes. These belong in the methods
  section of the writeup.

## Comparability guard — COMPLETE, reuse STANDS

H→H BRIEF-400 spot-check with the current (post-fix) harness: 2 tasks × 3
seeds = 6 runs, logged in `data_v3a_spotcheck/`.

| Task | V2 (brief) | Spot-check |
|------|-----------|------------|
| median_two_sorted | 2/3 | 3/3 (PASS, PASS, PASS) |
| n_queens | 0/3 | 1/3 (FAIL, PASS, FAIL) |
| **Total** | **16/24 (66.7%)** | **4/6 (66.7%)** |

Spot-check total is exactly 66.7% — within seed noise of V2's 66.7%. The V2
H→H reuse **stands**; no full-cell rerun needed. (Small upward drift on both
tasks, but total identical; n=6 is coarse.)
