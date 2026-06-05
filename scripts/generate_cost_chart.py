"""Generate a bar chart comparing token cost: claude-sonnet-4-6 vs claude-haiku-4-5."""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Anthropic public pricing (USD per 1M tokens, as of June 2026)
MODELS = [
    "claude-sonnet-4-6\n(previous)",
    "claude-haiku-4-5\n(current)",
]
INPUT_COST_PER_MTOK = [3.00, 0.80]   # $/MTok input
OUTPUT_COST_PER_MTOK = [15.00, 4.00]  # $/MTok output

# Typical book-pipeline token consumption (estimated from run logs)
INPUT_TOKENS_PER_RUN = 120_000   # ~120K input tokens per full pipeline run
OUTPUT_TOKENS_PER_RUN = 80_000   # ~80K output tokens per full pipeline run

total_costs = [
    (INPUT_COST_PER_MTOK[i] * INPUT_TOKENS_PER_RUN / 1_000_000)
    + (OUTPUT_COST_PER_MTOK[i] * OUTPUT_TOKENS_PER_RUN / 1_000_000)
    for i in range(len(MODELS))
]

savings_pct = (1 - total_costs[1] / total_costs[0]) * 100

x = np.arange(len(MODELS))
bar_width = 0.45

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(
    x,
    total_costs,
    width=bar_width,
    color=["#E07B54", "#4C9BE8"],
    edgecolor="white",
    linewidth=1.2,
)

# Value labels above each bar
for bar, cost in zip(bars, total_costs, strict=True):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.003,
        f"${cost:.3f}",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
    )

# Savings annotation
ax.annotate(
    f"↓ {savings_pct:.0f}% cost reduction",
    xy=(1, total_costs[1]),
    xytext=(1.25, (total_costs[0] + total_costs[1]) / 2),
    arrowprops={"arrowstyle": "->", "color": "#2ecc71", "lw": 1.8},
    fontsize=11,
    color="#2ecc71",
    fontweight="bold",
)

ax.set_xticks(x)
ax.set_xticklabels(MODELS, fontsize=11)
ax.set_ylabel("Estimated cost per pipeline run (USD)", fontsize=11)
ax.set_title(
    "Token Cost Optimisation: Sonnet 4.6 → Haiku 4.5\n"
    "crewai-latex-publisher • Hebrew Academic Book Pipeline",
    fontsize=12,
    fontweight="bold",
    pad=14,
)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.3f"))
ax.set_ylim(0, total_costs[0] * 1.35)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.5)

fig.tight_layout()

out_path = Path(__file__).parent.parent / "assets" / "cost_optimization.png"
out_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved: {out_path}")
