#!/usr/bin/env python3
"""Generate all matplotlib assets for 4 research articles."""
import matplotlib

matplotlib.use("Agg")

from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

from figures import article1, article2, article3, article4  # noqa: E402

rng = np.random.default_rng(42)

if __name__ == "__main__":
    article1.generate(Path("results/1_sine_wave/assets"),     rng)
    article2.generate(Path("results/2_security/assets"),      rng)
    article3.generate(Path("results/3_xlstm/assets"),         rng)
    article4.generate(Path("results/4_orchestration/assets"), rng)
    print("All 8 figures generated successfully.")
