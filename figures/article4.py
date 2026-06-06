"""Matplotlib figures for Article 4: Multi-Tool Orchestration."""
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


def generate(out: Path, rng: np.random.Generator) -> None:
    out.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis("off")
    events = [
        (0.08, "2022\nReAct",     "#FFD9B3"),
        (0.25, "2023\nToolFormer","#FFDDC1"),
        (0.42, "2023\nLangChain", "#C1E1FF"),
        (0.59, "2023\nAutoGen",   "#C1FFC1"),
        (0.76, "2024\nCrewAI",    "#E0C1FF"),
        (0.93, "2025\nFuture",    "#F5F5F5"),
    ]
    ax.axhline(0.5, color="#888", lw=2)
    for x, lbl, col in events:
        ax.add_patch(mpatches.Circle((x, 0.5), 0.045, fc=col, ec="#333",
            lw=1.5, transform=ax.transAxes, zorder=3))
        ax.text(x, 0.65, lbl, ha="center", va="bottom", fontsize=9,
                fontweight="bold", transform=ax.transAxes)
    ax.set_title("Evolution of Multi-Tool Orchestration in LLM Agents", fontsize=13)
    fig.tight_layout()
    fig.savefig(out / "architecture.png", dpi=150, bbox_inches="tight")
    plt.close()

    fig, ax = plt.subplots(figsize=(9, 5))
    agents = [1, 2, 4, 8, 16]
    serial_time   = [100, 180, 340, 660, 1300]
    parallel_time = [100, 105, 115, 145, 210]
    ax.plot(agents, serial_time,   "r-o", lw=2, ms=7, label="Sequential Execution")
    ax.plot(agents, parallel_time, "g-s", lw=2, ms=7, label="Parallel Orchestration")
    ax.set_xlabel("Number of Agents", fontsize=12)
    ax.set_ylabel("Total Latency (s)", fontsize=12)
    ax.set_title("Latency: Sequential vs Parallel Orchestration  (Python-generated)",
                 fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out / "results_graph.png", dpi=150, bbox_inches="tight")
    plt.close()
