# sameriver figure style
- facecolor #0f0f0f, text #e0e0e0, min font 11, dpi 200, constrained_layout=True, save bbox_inches='tight'
- Every title/label/annotation fully inside the saved image. After saving, OPEN the PNG and inspect: no clipped text, no overlapping labels, no legend covering data. Iterate until clean — never ship unviewed.
- Legends outside the axes unless there's clear dead space inside.
- Per-point text labels only when they cannot collide; otherwise encode with marker shape/color + legend.
- Model colors, always: Sonnet #6baed6, Haiku #d2a45f, GPT-4o-mini #9a9a9a, Qwen #8a7fd0. Red #e05252 reserved for failure/author marks.
- Captions live in the site's figcaption, not inside the image.
- One idea per figure; if it needs a paragraph to explain, split it.
