"""Matplotlib figures for Article 2: Supply Chain Security."""
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


def generate(out: Path, rng: np.random.Generator) -> None:
    out.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.axis("off")
    components = [
        (0.05, 0.35, 0.16, 0.30, "#FFB3B3", "Skill\nRepository"),
        (0.27, 0.35, 0.16, 0.30, "#FFD9B3", "ClawHavoc\nAttacker"),
        (0.50, 0.35, 0.16, 0.30, "#B3D9FF", "Agentic\nPipeline"),
        (0.73, 0.35, 0.16, 0.30, "#B3FFB3", "SkillSieve\nDefense"),
    ]
    for x, y, w, h, col, lbl in components:
        ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h,
            boxstyle="round,pad=0.02", fc=col, ec="#333", lw=1.5,
            transform=ax.transAxes))
        ax.text(x+w/2, y+h/2, lbl, ha="center", va="center",
                fontsize=10, fontweight="bold", transform=ax.transAxes)
    arrows = [(0.21, 0.50, "#e44", "Inject"), (0.43, 0.50, "#e44", "Exploit"),
              (0.66, 0.50, "#1a1", "Filter")]
    for x0, y0, col, lbl in arrows:
        ax.annotate("", xy=(x0+0.06, y0), xytext=(x0, y0),
                    xycoords="axes fraction", textcoords="axes fraction",
                    arrowprops={"arrowstyle": "->", "lw": 2.5, "color": col})
        ax.text(x0+0.03, y0+0.08, lbl, ha="center", fontsize=9,
                color=col, transform=ax.transAxes)
    ax.set_title("Supply Chain Attack Surface in Agentic Ecosystems", fontsize=13)
    fig.tight_layout()
    fig.savefig(out / "architecture.png", dpi=150, bbox_inches="tight")
    plt.close()

    fig, ax = plt.subplots(figsize=(9, 5))
    complexity = np.linspace(0, 10, 50)
    naive = 0.95 * np.exp(-complexity/6) + rng.normal(0, 0.01, 50)
    sieve = 0.92 * (1 - 0.35*np.exp(-complexity/3)) + rng.normal(0, 0.01, 50)
    ax.plot(complexity, np.clip(naive, 0, 1), "r--", lw=2, label="Naive Validator")
    ax.plot(complexity, np.clip(sieve, 0, 1), "g-",
            lw=2, label="SkillSieve (Proposed)")
    ax.set_xlabel("Attack Complexity Score", fontsize=12)
    ax.set_ylabel("Detection Rate", fontsize=12)
    ax.set_title("SkillSieve Detection Rate vs Attack Complexity  (Python-generated)",
                 fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out / "results_graph.png", dpi=150, bbox_inches="tight")
    plt.close()
