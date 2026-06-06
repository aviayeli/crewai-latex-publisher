"""Matplotlib figures for Article 3: Transformer vs xLSTM."""
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


def generate(out: Path, rng: np.random.Generator) -> None:
    out.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    arch_data = [
        ("Transformer (PatchTST)",
         ["Patch Embed", "Multi-Head\nAttention",
          "Feed-Forward", "Layer Norm", "Output"],
         ["#C1E1FF"] * 5),
        ("xLSTM",
         ["Input Proj", "sLSTM Block", "mLSTM Block", "Layer Norm", "Output"],
         ["#C1FFC1", "#FFE0B3", "#FFDDC1", "#E0C1FF", "#C1E1FF"]),
    ]
    for ax, (title, layers, colors) in zip(axes, arch_data, strict=False):
        ax.axis("off")
        for i, (lyr, col) in enumerate(zip(layers, colors, strict=False)):
            y = 0.85 - i * 0.18
            ax.add_patch(mpatches.FancyBboxPatch((0.15, y-0.06), 0.70, 0.12,
                boxstyle="round,pad=0.01", fc=col, ec="#555", lw=1.3,
                transform=ax.transAxes))
            ax.text(0.50, y, lyr, ha="center", va="center",
                    fontsize=9, fontweight="bold", transform=ax.transAxes)
            if i < len(layers) - 1:
                ax.annotate("", xy=(0.50, y-0.06), xytext=(0.50, y-0.12),
                            xycoords="axes fraction", textcoords="axes fraction",
                            arrowprops={"arrowstyle": "->", "lw": 1.5})
        ax.set_title(title, fontsize=12, fontweight="bold")
    fig.suptitle("Architecture Comparison: Transformer vs xLSTM", fontsize=13)
    fig.tight_layout()
    fig.savefig(out / "architecture.png", dpi=150, bbox_inches="tight")
    plt.close()

    fig, ax = plt.subplots(figsize=(9, 5))
    horizons = [96, 192, 336, 720]
    patch_mse  = [0.370, 0.413, 0.422, 0.447]
    xlstm_mse  = [0.355, 0.398, 0.411, 0.438]
    autoformer = [0.449, 0.500, 0.521, 0.564]
    x, w = np.arange(len(horizons)), 0.25
    ax.bar(x-w, patch_mse,  w, label="PatchTST",   color="#4472C4")
    ax.bar(x,   xlstm_mse,  w, label="xLSTM",      color="#ED7D31")
    ax.bar(x+w, autoformer, w, label="Autoformer", color="#A9D18E")
    ax.set_xticks(x)
    ax.set_xticklabels([f"H={h}" for h in horizons])
    ax.set_xlabel("Forecast Horizon", fontsize=12)
    ax.set_ylabel("MSE", fontsize=12)
    ax.set_title("MSE on ETTh1 Dataset Across Forecast Horizons  (Python-generated)",
                 fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out / "results_graph.png", dpi=150, bbox_inches="tight")
    plt.close()
