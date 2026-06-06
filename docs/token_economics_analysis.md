# Token Economics Analysis — Router-Skill

## Dr. Segal's Formula

$$WC_n = WC_{n-1} + Q_n + R_n + A_n$$

| Symbol | Meaning |
|--------|---------|
| $WC_n$ | Cumulative word/token count at round $n$ |
| $Q_n$  | Query tokens sent in round $n$ |
| $R_n$  | Result tokens received in round $n$ |
| $A_n$  | Agent-action tokens (skill load, routing overhead) |

## Eager vs Lazy Loading

In an **eager** pipeline (all skills loaded at startup), every round pays $A_{\text{eager}} = \sum_k C_{\text{load},k}$ regardless of whether the skill is used.

In the **Router-Skill** (lazy) approach, $A_n = C_{\text{load},k}$ only if skill $k$ is new in round $n$; subsequent uses cost $A_n = 0$ for that skill.

### Savings Formula

$$\Delta WC = \sum_{n=1}^{N} \mathbf{1}[\text{skill not needed in round } n] \cdot C_{\text{skill\_load}}$$

### Empirical Estimate (5 skills, 20 rounds, 40% average usage)

| Metric | Eager | Router-Skill |
|--------|-------|--------------|
| Skill-load tokens / round | 800 | 320 (avg) |
| Total over 20 rounds | 16 000 | 6 400 |
| **Savings** | — | **9 600 tokens (~60%)** |

## Implementation Notes

- `router_skill.py` uses `importlib.import_module` for lazy loading.
- `WCLedger.record(q, r, a)` applies the formula each round.
- `WCLedger.savings_vs_eager(eager_load_tokens)` computes the delta.
- `settings.MAX_ITER` (from `.env`) caps the amortized load cost estimate.
