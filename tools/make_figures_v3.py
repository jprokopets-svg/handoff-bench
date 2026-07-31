#!/usr/bin/env python3
"""Generate V3 figures for sameriver-site: work/the-handoff-study-part-ii.md.

F1 — Experiment A pass rates by model pair (neutral bars, H→H hatched as
     the reused Part I cell).
F2 — Experiment B three cells: paired pass / pre-write detection bars
     (detection bars absent for CLEAN, which has no planted lie).

Data verified against data_v3a/_progress.json, data_v3b/_progress.json,
and data_v2/_progress.json before writing this script.

Style per figure-style.md: #0f0f0f facecolor, #e0e0e0 text, min font 11,
dpi 200, constrained_layout, bbox_inches='tight', neutral #8a8f94 for
condition bars, accent #7aa5b8 for the non-model detection dimension,
hatching for reused/control cells, captions live in the site figcaption.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path("/Users/jakeprokopets/sameriver-site/site/figures")

BG = "#0f0f0f"
TEXT = "#e0e0e0"
NEUTRAL = "#8a8f94"
ACCENT = "#7aa5b8"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "text.color": TEXT,
    "axes.edgecolor": "#555",
    "axes.labelcolor": TEXT,
    "xtick.color": TEXT,
    "ytick.color": TEXT,
    "font.size": 11,
})

HATCH = "///"


def add_value_labels(ax, bars, fmt="%.1f%%", dy=1.5, color=TEXT, fs=12):
    for b in bars:
        patches = b.patches if hasattr(b, "patches") else [b]
        for p in patches:
            ax.text(p.get_x() + p.get_width() / 2, p.get_height() + dy,
                    fmt % p.get_height(), ha="center", va="bottom",
                    color=color, fontsize=fs)


# ── F1: Experiment A pass rates ───────────────────────────────────────
pairs = [("S\u2192S", 100.0), ("H\u2192S", 95.8), ("S\u2192H", 91.7), ("H\u2192H", 66.7)]
labels = [p[0] for p in pairs]
values = [p[1] for p in pairs]

fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
bars = []
for i, (lab, v) in enumerate(pairs):
    if lab == "H\u2192H":
        bars.append(ax.bar(i, v, 0.55, color=NEUTRAL, hatch=HATCH,
                           edgecolor="#666", linewidth=0.6,
                           label="Reused from Part I (V2)"))
    else:
        bars.append(ax.bar(i, v, 0.55, color=NEUTRAL, label="_nolegend_"))
add_value_labels(ax, bars)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels)
ax.set_ylim(0, 112)
ax.set_ylabel("Pass rate (%)")
ax.set_title("Experiment A — pass rate by model pair (BRIEF-400)", color=TEXT)
ax.legend(loc="upper left", frameon=False, bbox_to_anchor=(0.0, 1.12))
fig.savefig(OUT / "f1-v3-asymmetry.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ── F2: Experiment B pass + detection ─────────────────────────────────
cells = ["SUBTLE", "FLAGGED", "CLEAN"]
pass_rate = [58.3, 75.0, 66.7]
detect_rate = [95.8, 95.8, None]

fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
x = range(len(cells))
pass_bars = []
det_bars = []
for i, c in enumerate(cells):
    if c == "CLEAN":
        pass_bars.append(ax.bar(i, pass_rate[i], 0.32, color=NEUTRAL, hatch=HATCH,
                                edgecolor="#666", linewidth=0.6,
                                label="Pass rate (CLEAN = reused Part I baseline)"))
    else:
        pass_bars.append(ax.bar(i - 0.18, pass_rate[i], 0.32, color=NEUTRAL,
                                label="Pass rate" if i == 0 else "_nolegend_"))
    if detect_rate[i] is not None:
        det_bars.append(ax.bar(i + 0.18, detect_rate[i], 0.32, color=ACCENT,
                               label="Detected lie pre-write" if i == 0 else "_nolegend_"))
add_value_labels(ax, pass_bars)
add_value_labels(ax, det_bars)
ax.set_xticks(list(x))
ax.set_xticklabels(["Planted\n(subtle)", "Planted\n(flagged)", "Clean\n(no lie)"])
ax.set_ylim(0, 112)
ax.set_ylabel("Rate (%)")
ax.set_title("Experiment B — planted errors (H\u2192H, BRIEF-400)", color=TEXT)
ax.legend(loc="upper left", frameon=False, bbox_to_anchor=(0.0, 1.12))
fig.savefig(OUT / "f2-v3-planted.png", dpi=200, bbox_inches="tight")
plt.close(fig)

print("wrote", OUT / "f1-v3-asymmetry.png")
print("wrote", OUT / "f2-v3-planted.png")
