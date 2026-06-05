# crewai-latex-publisher

A multi-agent CrewAI pipeline that researches, writes, and compiles a
typeset Hebrew-English bilingual academic book on Transformer models — fully
automated from Perplexity research to a 15-page LuaLaTeX PDF.

---

## Architecture

```
Perplexity Research → Outline Planning → Markdown Generation (×6 chapters)
    → Pandoc Conversion → BiDi Validation → LuaLaTeX + Biber Compilation
```

Seven specialised agents collaborate via a hierarchical CrewAI process. Each
agent is injected with a domain-specific skill file from `skills/`. See
[`docs/PRD_latex_pipeline.md`](docs/PRD_latex_pipeline.md) for the complete
mechanism reference.

---

## Quick Start

```bash
cp .env.example .env       # add ANTHROPIC_API_KEY and PERPLEXITY_API_KEY
uv sync
uv run python main.py      # runs the full pipeline
```

Output PDF: `latex_output/main.pdf`

---

## Human-in-the-Loop (HITL) Gate

Before the 4-step LuaLaTeX + Biber compilation executes, the pipeline can
pause and require explicit operator approval. This gives a human the chance to
inspect the generated `.tex` files before committing compute to compilation.

**Enable the gate:**

```bash
# .env
HITL_ENABLED=true
```

When enabled, the terminal will display:

```
[HITL] Press Y to execute the 4-step PDF compilation for 'latex_output/main.tex' [Y/n]:
```

- Enter **Y** to proceed with compilation.
- Enter anything else to abort with a clear error message.

**Disabled by default** so automated CI runs and tests are unaffected.
The gate is implemented in `src/tools/lualatex_runner.py` and fully tested
in `tests/test_lualatex_runner.py`.

---

## LaTeX Pipeline — Mechanism Reference

Full documentation of every conversion step is in
[`docs/PRD_latex_pipeline.md`](docs/PRD_latex_pipeline.md), including:

- Pandoc CLI flags and `markdown+raw_tex` passthrough rationale
- Two-pattern `\textenglish{}` regex unescaping protocol
- 4-step LuaLaTeX / Biber compilation sequence
- Font stack: David CLM (Hebrew) · Courier New · Arial
- All `settings` fields and their defaults

---

## Cost Optimisation — 75% Token Cost Reduction

The pipeline was migrated from `claude-sonnet-4-6` to `claude-haiku-4-5`
without any quality regression on Hebrew academic text generation.

![Cost comparison bar chart: Sonnet 4.6 vs Haiku 4.5](assets/cost_optimization.png)

**Estimated per-run savings:**

| Model | Input $/MTok | Output $/MTok | Est. cost / run |
|---|---|---|---|
| claude-sonnet-4-6 (previous) | $3.00 | $15.00 | ~$1.56 |
| claude-haiku-4-5 (current)   | $0.80 | $4.00  | ~$0.42 |

> ~75% reduction in token spend with equivalent output quality for
> structured Hebrew academic text.

Model is configurable via `LLM_MODEL=` in `.env` — never hardcoded.

---

## Skills Inventory

| Skill file | Agent | Purpose |
|---|---|---|
| `skills/manager/SKILL.md` | ManagerAgent | Hierarchical orchestration |
| `skills/perplexity-research/SKILL.md` | ResearcherAgent | Perplexity API search |
| `skills/academic-outline/SKILL.md` | OutlineAgent | 6-chapter JSON outline |
| `skills/hebrew-academic-writing/SKILL.md` | ContentAgent | Hebrew prose writing |
| `skills/lualatex-bidi/SKILL.md` | BidiAgent | BiDi validation (10-item checklist) |
| `skills/matplotlib-tikz/SKILL.md` | FigureAgent | Chart and TikZ generation |
| `skills/lualatex-build/SKILL.md` | CompilerAgent | Pandoc → LuaLaTeX pipeline |
| `skills/latex_expert/SKILL.md` | CompilerAgent | Font injection + regex unescaping |

---

## Configuration

All tuneable values are set in `.env` (see `.env.example`). Key fields:

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Required |
| `PERPLEXITY_API_KEY` | — | Required |
| `LLM_MODEL` | `anthropic/claude-haiku-4-5-20251001` | Model for all agents |
| `MAX_AGENT_RETRIES` | `3` | Circuit breaker (3 strikes → halt) |
| `HITL_ENABLED` | `false` | Enable operator approval gate |
| `OUTPUT_DIR` | `latex_output` | Output directory |

---

## Testing

```bash
uv run ruff check .          # lint — must exit 0
uv run pytest --cov=src      # tests + coverage — must not decrease
wc -l src/**/*.py            # no src/ file may exceed 150 lines
```

Coverage is enforced by GitHub Actions CI on every push.

---

## Generating the Cost Chart

```bash
uv run python scripts/generate_cost_chart.py
# → assets/cost_optimization.png
```
