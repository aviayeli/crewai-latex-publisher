# TODO.md — Micro-Task Breakdown
## CrewAI LaTeX Publisher · Dr. Segal Vibe Coding Methodology

> **Methodology:** Every task is atomic, testable, and traceable to `docs/PLAN.md`. No task may be checked off without its gate check passing. TDD order is strictly enforced: the test file always precedes its implementation file.

---

## Phase 0: Project Bootstrap & Environment Setup

- [x] Verify `pyproject.toml` declares `crewai` as a dependency
- [x] Verify `pyproject.toml` declares `pydantic-settings` as a dependency
- [x] Verify `pyproject.toml` declares `ruff` as a dev dependency
- [x] Verify `pyproject.toml` declares `pytest` as a dev dependency
- [x] Verify `pyproject.toml` declares `pytest-cov` as a dev dependency
- [x] Verify `pyproject.toml` declares `matplotlib` as a dependency
- [x] Verify `pyproject.toml` declares `numpy` as a dependency
- [x] Run `uv sync` and confirm zero installation errors
- [x] Run `uv run python -c "import crewai"` — confirm exits 0
- [x] Run `uv run python -c "import pydantic_settings"` — confirm exits 0
- [x] Run `uv run python -c "import matplotlib"` — confirm exits 0
- [x] Run `uv run ruff --version` — confirm exits 0
- [x] Run `uv run pytest --version` — confirm exits 0
- [x] Create `.env.example` listing all 8 Settings fields with placeholder values
- [x] Create `.env` locally with real `ANTHROPIC_API_KEY` and confirm the file is gitignored
- [x] Confirm `.gitignore` excludes `.env`
- [x] Confirm `.gitignore` excludes `latex_output/*.pdf`
- [x] Confirm `.gitignore` excludes `latex_output/chapters/*.tex`
- [x] Confirm `.gitignore` excludes `latex_output/assets/*.png`
- [x] Add `[tool.ruff]` section to `pyproject.toml` with `line-length = 88`
- [x] Add `select = ["E", "F", "I"]` to `[tool.ruff]` section in `pyproject.toml`
- [x] Add `[tool.pytest.ini_options]` section with `addopts = "--cov=src"` to `pyproject.toml`
- [x] Add `markers = ["slow: end-to-end tests requiring API key and lualatex binary"]` to pytest config
- [x] Create `src/__init__.py` as an empty file
- [x] Create `src/agents/__init__.py` as an empty file
- [x] Create `src/tasks/__init__.py` as an empty file
- [x] Create `src/tools/__init__.py` as an empty file
- [x] Create `latex_output/.gitkeep`
- [x] Create `latex_output/assets/.gitkeep`
- [x] Create `latex_output/chapters/.gitkeep`
- [x] Create `latex_output/figures/.gitkeep`
- [x] Run `uv run pytest tests/` — confirm "no tests collected" without error
- [x] Run `uv run ruff check .` — confirm exits 0 on the empty source tree

---

## Phase 1: SKILL.md Authoring — `skills/academic-outline/SKILL.md`

- [x] Create directory `skills/academic-outline/`
- [x] Create `skills/academic-outline/SKILL.md` with a header section declaring the agent role as Academic Outline Architect
- [x] Write the full JSON schema for `book_outline.json` inside this SKILL.md (fields: `title`, `subtitle`, `chapters` array, each with `number`, `hebrew_title`, `english_title`, `page_budget`, `sections`)
- [x] Document chapter planning convention: chapters ordered thematically, not chronologically
- [x] Document the constraint that `page_budget` values across all 6 chapters must sum to exactly 15
- [x] Document that the outline must include a `refs` field listing at minimum 6 BibTeX citation keys
- [x] Document citation norms: every factual claim in the book requires a `\cite{}` key sourced from `refs.bib`
- [x] Document that `book_outline.json` must be valid JSON with no trailing commas or comments
- [x] Document that the output path must be exactly `latex_output/book_outline.json`
- [x] Write a complete worked JSON example in the SKILL.md showing all required fields populated
- [x] Verify `skills/academic-outline/SKILL.md` is non-empty (`wc -c` > 0)
- [x] Verify `skills/academic-outline/SKILL.md` contains the string `book_outline.json`
- [x] Verify `skills/academic-outline/SKILL.md` contains the string `page_budget`
- [x] Verify `skills/academic-outline/SKILL.md` contains the string `hebrew_title`

---

## Phase 1 continued: `skills/hebrew-academic-writing/SKILL.md`

- [x] Create directory `skills/hebrew-academic-writing/`
- [x] Create `skills/hebrew-academic-writing/SKILL.md` with header declaring the agent role as Hebrew Academic Writer
- [x] Document Hebrew academic register: formal tone, third person, passive constructions where appropriate
- [x] Document the `\textenglish{}` macro: explain when to wrap an English term inside a Hebrew RTL paragraph
- [x] Document the rule that proper nouns and model names (Transformer, BERT, GPT) are never translated — kept in English
- [x] Document RTL paragraph structure: content inside `\begin{hebrew}...\end{hebrew}` block when needed
- [x] Document that each chapter `.tex` file must NOT contain `\begin{document}` or `\end{document}`
- [x] Document that chapter files must use `\chapter{}` as the top-level structural command
- [x] Document that inline math must use `\(` and `\)` delimiters (not bare `$`) in LuaLaTeX BiDi mode
- [x] Document that display math must use `\begin{equation}` (not `$$`)
- [x] Document page budget enforcement: ContentAgent must target the `page_budget` from `book_outline.json`
- [x] Document a list of at least 5 forbidden Hebrew typographic errors (wrong quote marks, improper dagesh usage, missing maqaf)
- [x] Write a 3-sentence example Hebrew academic paragraph with `\textenglish{}` usage directly in the SKILL.md
- [x] Verify `skills/hebrew-academic-writing/SKILL.md` contains the string `\textenglish`
- [x] Verify `skills/hebrew-academic-writing/SKILL.md` contains the string `\chapter`

---

## Phase 1 continued: `skills/perplexity-research/SKILL.md`

- [ ] Create directory `skills/perplexity-research/`
- [ ] Create `skills/perplexity-research/SKILL.md` with header declaring the agent role as Academic Researcher
- [ ] Document the Perplexity AI API: OpenAI-compatible `/chat/completions` endpoint, model `sonar-pro`, `Bearer` token auth via `PERPLEXITY_API_KEY`
- [ ] Document query formulation for academic sources: use precise technical terminology, specify publication year range, name specific authors or papers where known
- [ ] Document how to distinguish primary sources (peer-reviewed papers) from secondary sources (blog posts, documentation) in results
- [ ] Document the output format expected from the Research Agent: a structured Markdown block with citation keys, titles, authors, years, and 2-sentence summaries per source
- [ ] Document that research output must map to BibTeX keys in `refs.bib` — the Researcher Agent populates the citation key list used by downstream agents
- [ ] Document rate-limit handling: if Perplexity returns HTTP 429, the agent must wait and retry; do not propagate the error silently
- [ ] Write a worked example query and response demonstrating correct output format
- [ ] Verify `skills/perplexity-research/SKILL.md` contains the string `sonar-pro`
- [ ] Verify `skills/perplexity-research/SKILL.md` contains the string `PERPLEXITY_API_KEY`

---

## Phase 1 continued: `skills/manager/SKILL.md`

- [ ] Create directory `skills/manager/`
- [ ] Create `skills/manager/SKILL.md` with header declaring the agent role as Project Manager
- [ ] Document the Manager Agent's sole responsibility: coordinate task delegation; it never writes files or calls external APIs directly
- [ ] Document the delegation strategy: assign each task to the sub-agent whose role and tools best match the task requirements
- [ ] Document the sub-agent capability matrix: for each of the 6 worker agents, list what tasks it can handle and what tools it has
- [ ] Document the retry policy: if a sub-agent's task output fails validation, re-delegate the same task to the same agent with additional guidance, up to `MAX_AGENT_RETRIES` attempts
- [ ] Document escalation: if a task fails after all retries, log the failure reason in the task output and proceed — do not block the entire pipeline
- [ ] Document that the Manager Agent must set `allow_delegation=True` and must not be listed in the worker `agents=[]` list
- [ ] Verify `skills/manager/SKILL.md` contains the string `allow_delegation`
- [ ] Verify `skills/manager/SKILL.md` contains the string `delegate`

---

## Phase 1 continued: `skills/lualatex-bidi/SKILL.md`

- [ ] Create directory `skills/lualatex-bidi/`
- [ ] Create `skills/lualatex-bidi/SKILL.md` with header declaring the agent role as LaTeX BiDi Typesetting Specialist
- [ ] Document the `bidi` package: explain that it is automatically loaded by `polyglossia` when Hebrew is set as main language
- [ ] Document `polyglossia` language switching: `\setmainlanguage{hebrew}` and `\setotherlanguage{english}`
- [ ] Document the `\textenglish{}` command for inline English within Hebrew RTL paragraphs
- [ ] Document the `\begin{english}...\end{english}` environment for multi-line English blocks
- [ ] Document the `\begin{LTR}...\end{LTR}` environment for left-to-right code or data blocks
- [ ] Document the three mandatory BiDi constructs required in Chapter 3: (1) RTL paragraph with inline `\textenglish{}`, (2) LTR `equation` environment, (3) `\begin{LTR}...\end{LTR}` block
- [ ] Document common RTL/LTR pitfall: punctuation mirroring artifacts in BiDi mode and how to fix them
- [ ] Write a validation checklist of at least 10 items an agent must verify before marking a chapter as BiDi-clean
- [ ] Document that BidiAgent must validate all 6 chapters, not only Chapter 3
- [ ] Document the fix procedure: how to insert missing BiDi constructs without breaking surrounding context
- [ ] Write a concrete example of a BiDi-correct paragraph in the SKILL.md
- [ ] Write a concrete example of a common BiDi mistake paired with its corrected form
- [ ] Verify `skills/lualatex-bidi/SKILL.md` contains the string `\setmainlanguage`
- [ ] Verify `skills/lualatex-bidi/SKILL.md` contains the string `\begin{LTR}`

---

## Phase 1 continued: `skills/matplotlib-tikz/SKILL.md`

- [ ] Create directory `skills/matplotlib-tikz/`
- [ ] Create `skills/matplotlib-tikz/SKILL.md` with header declaring the agent role as Scientific Figure Generator
- [ ] Document matplotlib save-as-PNG at 300 dpi: `plt.savefig(path, dpi=300, bbox_inches='tight')`
- [ ] Document that the output path must be exactly `latex_output/assets/attention_complexity.png`
- [ ] Document axis labeling requirements: x-axis = "Sequence Length (n)", y-axis = "Complexity", legend required
- [ ] Document the three curves the plot must display: O(n²) standard attention, O(n log n) linear attention, O(n) recurrent
- [ ] Document that the matplotlib script must import only from `matplotlib.pyplot` and `numpy` (no other imports)
- [ ] Document TikZ syntax for scaled dot-product attention formula diagram with Q, K, V nodes
- [ ] Document the output path for the TikZ snippet: `latex_output/figures/sdp_attention.tex`
- [ ] Document how to connect TikZ nodes with arrows to represent the SDP attention data flow
- [ ] Document `\includegraphics` integration: the LaTeX command to embed the PNG in a figure environment
- [ ] Write the complete expected matplotlib script structure (with comments for each section) in the SKILL.md
- [ ] Write the complete expected TikZ skeleton for `sdp_attention.tex` in the SKILL.md
- [ ] Verify `skills/matplotlib-tikz/SKILL.md` contains the string `dpi=300`
- [ ] Verify `skills/matplotlib-tikz/SKILL.md` contains the string `sdp_attention.tex`

---

## Phase 1 continued: `skills/lualatex-build/SKILL.md`

- [ ] Create directory `skills/lualatex-build/`
- [ ] Create `skills/lualatex-build/SKILL.md` with header declaring the agent role as LaTeX Build Engineer
- [ ] Document the exact `lualatex` CLI flags to use: `--interaction=nonstopmode` and `--output-directory`
- [ ] Document the two-pass compilation strategy and why it is required (cross-references, bibliography)
- [ ] Document the required preamble package list: `fontspec`, `polyglossia`, `biblatex`, `geometry`, `graphicx`, `amsmath`, `hyperref`, `tikz`, `booktabs`, `xcolor`
- [ ] Document `\documentclass[17pt,a4paper]{extarticle}` as the document class declaration
- [ ] Document `fontspec` usage and the Hebrew font fallback chain: `David CLM` → `Frank Ruehl CLM` → `Noto Serif Hebrew`
- [ ] Document that `polyglossia` must be used as the language package (not `babel`)
- [ ] Document `biblatex` configuration: `backend=biber`, `addbibresource{refs.bib}`
- [ ] Document the `\input{}` ordering convention: `chapters/ch1` through `chapters/ch6` in sequence
- [ ] Document `\printbibliography` placement at the end of the document body before `\end{document}`
- [ ] Document log parsing heuristics: lines beginning with `! LaTeX Error` or `! Undefined control sequence`
- [ ] Document that the assembled `main.tex` must be written to `latex_output/main.tex`
- [ ] Document the Markdown-first workflow: ContentAgent writes each chapter as `ch{n}.md` first, then calls `markdown_converter_tool` (pandoc) to produce `ch{n}.tex`; the Compiler Agent operates only on the resulting `.tex` files
- [ ] Document the three-step biber compilation pipeline: (1) `lualatex main.tex` — generates `.bcf`; (2) `biber main` — resolves bibliography from `refs.bib`; (3) `lualatex main.tex` — incorporates `.bbl` and resolves cross-references
- [ ] Document `biber` CLI invocation: `biber <stem>` where stem is the `.tex` filename without extension (e.g., `biber main`)
- [ ] Document that `biblatex` must be loaded with `backend=biber` in the preamble — using `backend=bibtex` will break the pipeline
- [ ] Document the `BIBER_BIN` and `PANDOC_BIN` settings fields as the configurable binary paths
- [ ] Write the complete preamble skeleton (10–15 lines of actual LaTeX) in the SKILL.md
- [ ] Write the complete `main.tex` body skeleton showing all 6 `\input{}` calls in the SKILL.md
- [ ] Verify `skills/lualatex-build/SKILL.md` contains the string `nonstopmode`
- [ ] Verify `skills/lualatex-build/SKILL.md` contains the string `polyglossia`
- [ ] Verify `skills/lualatex-build/SKILL.md` contains the string `\printbibliography`
- [ ] Verify `skills/lualatex-build/SKILL.md` contains the string `biber`
- [ ] Verify `skills/lualatex-build/SKILL.md` contains the string `pandoc`

---

## Phase 2: Test Infrastructure — `tests/conftest.py`

- [ ] Create `tests/conftest.py` with imports: `pytest`, `pathlib.Path`, `unittest.mock`
- [ ] Write `tmp_output_dir` fixture with `scope="function"` using `tmp_path`
- [ ] In `tmp_output_dir`: create `assets/` subdirectory inside the temp path
- [ ] In `tmp_output_dir`: create `chapters/` subdirectory inside the temp path
- [ ] In `tmp_output_dir`: create `figures/` subdirectory inside the temp path
- [ ] In `tmp_output_dir`: patch `src.config.settings.OUTPUT_DIR` to point at the temp path string
- [ ] In `tmp_output_dir`: patch `src.config.settings.ASSETS_DIR` to point at `tmp_path / "assets"` string
- [ ] In `tmp_output_dir`: `yield` the temp path, then allow teardown to happen automatically
- [ ] Write `mock_settings` fixture: construct a `Settings` instance with test values, no `.env` required
- [ ] In `mock_settings`: set `LLM_MODEL = "claude-haiku-4-5-20251001"` for speed in unit tests
- [ ] In `mock_settings`: set `ANTHROPIC_API_KEY = "test-key-placeholder"`
- [ ] In `mock_settings`: set `MAX_AGENT_RETRIES = 1`
- [ ] In `mock_settings`: set `PYTHON_RUNNER_TIMEOUT_S = 10`
- [ ] Verify `tests/conftest.py` is ≤ 40 lines: run `wc -l tests/conftest.py`
- [ ] Run `uv run ruff check tests/conftest.py` — confirm exits 0

---

## Phase 3: TDD — Write Failing Tests for `src/config.py`

> Gate: `src/config.py` must NOT exist yet. All tests in this phase must fail with ImportError.

- [ ] Create `tests/test_config.py` with imports: `pytest`, `os`, `unittest.mock.patch`
- [ ] Write `test_settings_load_from_env`: monkeypatch `ANTHROPIC_API_KEY=sk-test`, import `Settings`, assert `Settings(ANTHROPIC_API_KEY="sk-test").ANTHROPIC_API_KEY == "sk-test"`
- [ ] Write `test_llm_model_default`: assert `Settings(ANTHROPIC_API_KEY="x").LLM_MODEL == "claude-sonnet-4-6"`
- [ ] Write `test_max_agent_retries_default`: assert `Settings(ANTHROPIC_API_KEY="x").MAX_AGENT_RETRIES == 3`
- [ ] Write `test_python_runner_timeout_default`: assert `Settings(ANTHROPIC_API_KEY="x").PYTHON_RUNNER_TIMEOUT_S == 60`
- [ ] Write `test_lualatex_bin_default`: assert `Settings(ANTHROPIC_API_KEY="x").LUALATEX_BIN == "lualatex"`
- [ ] Write `test_output_dir_default`: assert `Settings(ANTHROPIC_API_KEY="x").OUTPUT_DIR == "latex_output"`
- [ ] Write `test_assets_dir_default`: assert `Settings(ANTHROPIC_API_KEY="x").ASSETS_DIR == "latex_output/assets"`
- [ ] Write `test_min_pages_default`: assert `Settings(ANTHROPIC_API_KEY="x").MIN_PAGES == 15`
- [ ] Write `test_missing_api_key_raises`: assert constructing `Settings()` with no `ANTHROPIC_API_KEY` in env raises `ValidationError`
- [ ] Write `test_missing_perplexity_api_key_raises`: assert constructing `Settings()` with no `PERPLEXITY_API_KEY` raises `ValidationError`
- [ ] Write `test_perplexity_api_key_loaded`: monkeypatch `PERPLEXITY_API_KEY=pplx-test`; assert `Settings(...).PERPLEXITY_API_KEY == "pplx-test"`
- [ ] Write `test_biber_bin_default`: assert `Settings(...).BIBER_BIN == "biber"`
- [ ] Write `test_pandoc_bin_default`: assert `Settings(...).PANDOC_BIN == "pandoc"`
- [ ] Write `test_env_override_llm_model`: monkeypatch `LLM_MODEL=claude-opus-4-8`; assert `LLM_MODEL` picks up the override
- [ ] Write `test_env_override_min_pages`: monkeypatch `MIN_PAGES=20`; assert `MIN_PAGES == 20`
- [ ] Confirm `uv run pytest tests/test_config.py` exits non-zero (ImportError — `src/config.py` absent)
- [ ] Run `uv run ruff check tests/test_config.py` — confirm exits 0

---

## Phase 4: TDD — Write Failing Tests for `src/tools/latex_writer.py`

> Gate: `src/tools/latex_writer.py` must NOT exist yet. All tests must fail with ImportError.

- [ ] Create `tests/test_latex_writer.py` with imports: `pytest`, `pathlib.Path`, `src.tools.latex_writer` (will fail at import)
- [ ] Write `test_write_creates_file`: call `latex_writer_tool._run(path="chapters/ch1.tex", content="\\chapter{Test}", mode="write")`; assert the file exists with exact content
- [ ] Write `test_write_overwrites_existing_file`: call `_run` twice with different content in write mode; assert only the second content remains
- [ ] Write `test_append_adds_content`: write then append; assert the file contains both strings concatenated
- [ ] Write `test_append_to_nonexistent_creates_file`: append to a new path; assert file is created with the content
- [ ] Write `test_path_traversal_rejected_dotdot`: call with `path="../../../etc/passwd"`; assert `ValueError` is raised
- [ ] Write `test_path_traversal_rejected_absolute_path`: call with an absolute path outside `OUTPUT_DIR`; assert `ValueError`
- [ ] Write `test_creates_parent_directories`: write to `chapters/sub/deep/ch1.tex`; assert parent directories were created automatically
- [ ] Write `test_utf8_encoding_hebrew`: write Hebrew string `"שלום עולם"`; read file back and assert it equals the original string
- [ ] Write `test_return_value_contains_path`: assert the string returned by `_run` contains the resolved file path
- [ ] Write `test_write_empty_string`: write empty content in write mode; assert file exists and has zero bytes
- [ ] Write `test_mode_invalid_raises_validation_error`: call with `mode="overwrite"` (not in `Literal`); assert `ValidationError` or `ValueError`
- [ ] Write `test_tool_name_attribute`: assert `latex_writer_tool.name == "latex_writer"`
- [ ] Write `test_args_schema_has_path_field`: introspect `LatexWriterInput.model_fields`; assert `"path"` is present
- [ ] Write `test_args_schema_has_content_field`: assert `"content"` is present in `LatexWriterInput.model_fields`
- [ ] Write `test_args_schema_has_mode_field`: assert `"mode"` is present in `LatexWriterInput.model_fields`
- [ ] Confirm `uv run pytest tests/test_latex_writer.py` exits non-zero (ImportError)
- [ ] Run `uv run ruff check tests/test_latex_writer.py` — confirm exits 0

---

## Phase 4.5: TDD — Write Failing Tests for `src/tools/perplexity_search.py`

> Gate: `src/tools/perplexity_search.py` must NOT exist yet. All tests must fail with ImportError.

- [ ] Create `tests/test_perplexity_search.py` with imports: `pytest`, `unittest.mock`, `src.tools.perplexity_search`
- [ ] Write `test_tool_name_attribute`: assert `perplexity_search_tool.name == "perplexity_search"`
- [ ] Write `test_args_schema_has_query_field`: assert `"query"` is in `PerplexitySearchInput.model_fields`
- [ ] Write `test_empty_query_raises`: call `_run(query="", max_results=3)`; assert `ValueError` is raised
- [ ] Write `test_request_sent_to_perplexity_endpoint`: mock `requests.post`; call `_run(query="transformers")`; assert the mocked `post` was called with a URL containing `perplexity.ai`
- [ ] Write `test_bearer_token_in_headers`: mock `requests.post`; assert `Authorization` header in the call kwargs starts with `"Bearer "`
- [ ] Write `test_returns_string_on_success`: mock `requests.post` to return a fixture JSON response; assert return value is a `str`
- [ ] Write `test_http_error_raises`: mock `requests.post` to return status 401; assert `ValueError` or `requests.HTTPError` is raised
- [ ] Write `test_rate_limit_429_raises`: mock `requests.post` to return status 429; assert the raised exception signals a rate-limit condition
- [ ] Confirm `uv run pytest tests/test_perplexity_search.py` exits non-zero (ImportError)
- [ ] Run `uv run ruff check tests/test_perplexity_search.py` — confirm exits 0

---

## Phase 4.6: TDD — Write Failing Tests for `src/tools/markdown_converter.py`

> Gate: `src/tools/markdown_converter.py` must NOT exist yet. All tests must fail with ImportError.

- [ ] Create `tests/test_markdown_converter.py` with imports: `pytest`, `pathlib.Path`, `shutil`, `unittest.mock`, `src.tools.markdown_converter`
- [ ] Write `test_tool_name_attribute`: assert `markdown_converter_tool.name == "markdown_converter"`
- [ ] Write `test_args_schema_has_md_path_field`: assert `"md_path"` is in `MarkdownConverterInput.model_fields`
- [ ] Write `test_args_schema_has_tex_path_field`: assert `"tex_path"` is in `MarkdownConverterInput.model_fields`
- [ ] Write `test_path_traversal_md_rejected`: call with `md_path="../escape.md"`; assert `ValueError`
- [ ] Write `test_path_traversal_tex_rejected`: call with `tex_path="../../etc/evil.tex"`; assert `ValueError`
- [ ] Write `test_return_value_contains_output_path`: mock `subprocess.run`; assert return string includes the resolved `.tex` path
- [ ] Write `test_pandoc_called_with_correct_flags`: mock `subprocess.run`; assert call includes `"-f"`, `"markdown"`, `"-t"`, `"latex"`, and `"-o"`
- [ ] Write `test_pandoc_not_found_raises`: patch `settings.PANDOC_BIN = "nonexistent-binary-xyz"`; assert `FileNotFoundError` or `OSError` is raised
- [ ] Decorate a conditional integration test class: `@pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc not installed")`
- [ ] Write `test_real_markdown_converts_to_tex` inside that class: write a temp `.md` file; call `_run`; assert `.tex` output file exists and is non-empty
- [ ] Confirm `uv run pytest tests/test_markdown_converter.py` exits non-zero (ImportError)
- [ ] Run `uv run ruff check tests/test_markdown_converter.py` — confirm exits 0

---

## Phase 5: TDD — Write Failing Tests for `src/tools/python_runner.py`

> Gate: `src/tools/python_runner.py` must NOT exist yet. All tests must fail with ImportError.

- [ ] Create `tests/test_python_runner.py` with imports: `pytest`, `pathlib.Path`, `src.tools.python_runner`
- [ ] Write `test_valid_simple_script_executes`: run script `print("hello")`; assert return value contains `"hello"`
- [ ] Write `test_valid_matplotlib_script_produces_png`: run a script that imports `matplotlib.pyplot` and `numpy` and saves a PNG to `tmp_output_dir`; assert the PNG file exists
- [ ] Write `test_disallowed_import_subprocess_rejected`: script contains `import subprocess`; assert `ValueError` is raised before execution
- [ ] Write `test_disallowed_import_sys_rejected`: script contains `import sys`; assert `ValueError` is raised
- [ ] Write `test_disallowed_import_shutil_rejected`: script contains `import shutil`; assert `ValueError` is raised
- [ ] Write `test_disallowed_import_requests_rejected`: script contains `import requests`; assert `ValueError` is raised
- [ ] Write `test_allowed_import_numpy_passes_scan`: script contains `import numpy`; assert `_scan_imports` returns an empty list
- [ ] Write `test_allowed_import_pathlib_passes_scan`: script contains `from pathlib import Path`; assert `_scan_imports` returns an empty list
- [ ] Write `test_allowed_import_os_passes_scan`: script contains `import os`; assert `_scan_imports` returns an empty list
- [ ] Write `test_ast_scan_catches_from_import_disallowed_module`: script contains `from requests import get`; assert `ValueError` (requests not in allowed set)
- [ ] Write `test_timeout_enforced`: script contains an infinite loop `while True: pass`; assert a timeout-related exception is raised within `PYTHON_RUNNER_TIMEOUT_S` seconds
- [ ] Write `test_syntax_error_reported`: script contains `def foo(:` (invalid syntax); assert the return value contains stderr output and does not raise unhandled exception
- [ ] Write `test_import_whitelist_is_frozenset`: assert `type(ALLOWED_IMPORTS) is frozenset`
- [ ] Write `test_scan_detects_multiple_bad_imports`: script has `import subprocess\nimport requests`; assert `ValueError` message references both disallowed names
- [ ] Write `test_tool_name_attribute`: assert `python_runner_tool.name == "python_runner"`
- [ ] Write `test_script_stdout_captured`: script prints a unique UUID string; assert that exact string appears in the return value
- [ ] Confirm `uv run pytest tests/test_python_runner.py` exits non-zero (ImportError)
- [ ] Run `uv run ruff check tests/test_python_runner.py` — confirm exits 0

---

## Phase 6: TDD — Write Failing Tests for `src/tools/lualatex_runner.py`

> Gate: `src/tools/lualatex_runner.py` must NOT exist yet. All tests must fail with ImportError.

- [ ] Create `tests/test_lualatex_runner.py` with imports: `pytest`, `shutil`, `pathlib.Path`, `src.tools.lualatex_runner`
- [ ] Write `test_compilation_error_is_exception_subclass`: assert `issubclass(CompilationError, Exception)`
- [ ] Write `test_log_parser_detects_error_line`: create a string containing `"! LaTeX Error: File not found"`; write to a temp file; call `tool._parse_log(path)`; assert returned list is non-empty
- [ ] Write `test_log_parser_clean_log_returns_empty_list`: create a log string with no `!` error lines; call `_parse_log`; assert returned list is empty
- [ ] Write `test_log_parser_detects_undefined_control_sequence`: feed `"! Undefined control sequence."` in log; assert it is captured
- [ ] Write `test_log_parser_ignores_info_lines`: log contains only `"This is LuaTeX, ..."` info lines; assert empty list returned
- [ ] Write `test_build_cmd_contains_nonstopmode`: call `tool._build_cmd("main.tex")`; assert `"--interaction=nonstopmode"` is in the result list
- [ ] Write `test_build_cmd_contains_output_directory_flag`: assert the result of `_build_cmd` contains a string starting with `"--output-directory="`
- [ ] Write `test_build_cmd_contains_tex_filename`: assert `"main.tex"` is in `_build_cmd("main.tex")`
- [ ] Write `test_build_cmd_first_element_is_lualatex_bin`: assert `_build_cmd("main.tex")[0] == settings.LUALATEX_BIN`
- [ ] Write `test_tool_name_attribute`: assert `lualatex_runner_tool.name == "lualatex_runner"`
- [ ] Write `test_default_passes_is_two`: instantiate `LualatexRunnerInput(tex_file="main.tex")`; assert `.passes == 2`
- [ ] Write `test_default_run_biber_is_true`: instantiate `LualatexRunnerInput(tex_file="main.tex")`; assert `.run_biber == True`
- [ ] Write `test_build_biber_cmd_contains_biber_bin`: assert `_build_biber_cmd("main")[0] == settings.BIBER_BIN`
- [ ] Write `test_build_biber_cmd_contains_stem`: assert `"main"` is in `_build_biber_cmd("main")`
- [ ] Write `test_biber_called_between_lualatex_passes`: mock `subprocess.run`; call `_run("main.tex", passes=2, run_biber=True)`; assert mock call order is lualatex → biber → lualatex
- [ ] Write `test_biber_skipped_when_run_biber_false`: mock `subprocess.run`; call `_run("main.tex", passes=2, run_biber=False)`; assert biber command never called
- [ ] Decorate an integration test class with `@pytest.mark.skipif(shutil.which("lualatex") is None, reason="lualatex not installed")`
- [ ] Write `test_minimal_tex_compiles_successfully` inside that class: write a minimal valid `.tex` file to tmp dir; call `_run`; assert return dict has `"success": True`
- [ ] Write `test_invalid_tex_raises_compilation_error` inside that class: write syntactically broken LaTeX; assert `CompilationError` is raised
- [ ] Confirm `uv run pytest tests/test_lualatex_runner.py` exits non-zero (ImportError)
- [ ] Run `uv run ruff check tests/test_lualatex_runner.py` — confirm exits 0

---

## Phase 7: TDD — Write Failing Tests for `src/crew.py`

> Gate: `src/crew.py` and all agent/task modules must NOT exist yet. All tests must fail with ImportError.

- [ ] Create `tests/test_crew.py` with imports: `pytest`, `unittest.mock`, `pathlib.Path`, `src.crew`
- [ ] Write `test_load_skill_reads_file`: write a temp `SKILL.md` in a temp skills dir; call `_load_skill`; assert returned string matches file content
- [ ] Write `test_load_skill_missing_raises_file_not_found`: call `_load_skill("nonexistent-skill-xyz")`; assert `FileNotFoundError`
- [ ] Write `test_load_skill_reads_from_skills_subdir`: mock `Path.read_text`; verify `_load_skill("foo")` constructs path `skills/foo/SKILL.md`
- [ ] Write `test_publisher_crew_init_loads_seven_skills`: mock `_load_skill` to return dummy strings; construct `PublisherCrew()`; assert mock called exactly 7 times
- [ ] Write `test_all_agent_backstories_equal_skill_content`: mock all 7 SKILL.md reads with distinct strings; construct `PublisherCrew()`; assert each agent's `backstory` equals its corresponding mock return value
- [ ] Write `test_no_agent_backstory_is_hardcoded_python_string`: assert no agent module file contains a string literal that would serve as the backstory (prove skills are loaded from files, not inline)
- [ ] Write `test_crew_has_exactly_eleven_tasks`: construct `PublisherCrew()` with mocked skills; collect all tasks; assert count `== 11`
- [ ] Write `test_crew_has_exactly_seven_agents`: assert all seven agent attributes (manager + 6 workers) are present and distinct
- [ ] Write `test_outline_task_has_no_context`: assert `crew.outline_task.context` is empty or `None`
- [ ] Write `test_content_tasks_each_have_outline_in_context`: assert `outline_task` appears in each content task's `context`
- [ ] Write `test_bidi_task_context_contains_all_six_content_tasks`: assert `len(crew.bidi_task.context) == 6`
- [ ] Write `test_figure_task_context_contains_outline_task`: assert `crew.outline_task in crew.figure_task.context`
- [ ] Write `test_compile_task_context_contains_bidi_and_figure`: assert both `bidi_task` and `figure_task` appear in `compile_task.context`
- [ ] Write `test_all_agents_llm_matches_settings`: assert each agent's `llm` attribute equals `settings.LLM_MODEL`
- [ ] Write `test_all_agents_max_retry_matches_settings`: assert each agent's `max_retry_limit == settings.MAX_AGENT_RETRIES`
- [ ] Write `test_missing_skill_file_prevents_crew_init`: mock one skill file as missing; assert `PublisherCrew()` raises `FileNotFoundError`
- [ ] Write `test_kickoff_constructs_hierarchical_crew`: mock `Crew.kickoff`; call `PublisherCrew().kickoff()`; assert `Crew` was constructed with `process=Process.hierarchical`
- [ ] Write `test_manager_agent_passed_as_kwarg`: mock `Crew`; assert `Crew(...)` was called with `manager_agent=` kwarg and that the manager agent is NOT in the `agents=` list
- [ ] Write `test_manager_agent_allow_delegation_true`: assert `crew.manager_agent.allow_delegation == True`
- [ ] Write `test_research_task_has_no_context`: assert `crew.research_task.context` is empty or `None`
- [ ] Write `test_outline_task_context_contains_research_task`: assert `crew.research_task in crew.outline_task.context`
- [ ] Confirm `uv run pytest tests/test_crew.py` exits non-zero (ImportError)
- [ ] Run `uv run ruff check tests/test_crew.py` — confirm exits 0

---

## Phase 8: TDD — Write Failing Tests for `tests/test_integration.py`

> Gate: Implementation must NOT be complete yet. Tests must be skipped or fail.

- [ ] Create `tests/test_integration.py` with imports: `pytest`, `pathlib.Path`, `shutil`, `json`, `subprocess`
- [ ] Add module-level `pytestmark = pytest.mark.slow`
- [ ] Add a session-scoped `skipif` guard: skip all tests if `ANTHROPIC_API_KEY` is absent from environment or `lualatex` binary is absent
- [ ] Write `test_full_pipeline_produces_pdf`: call `PublisherCrew().kickoff()`; assert `Path("latex_output/main.pdf").exists()`
- [ ] Write `test_pdf_has_minimum_fifteen_pages`: run `pdfinfo latex_output/main.pdf` via subprocess; parse the `Pages:` line; assert value `>= 15`
- [ ] Write `test_all_six_chapter_files_exist`: assert each of `ch1.tex` through `ch6.tex` exists in `latex_output/chapters/`
- [ ] Write `test_book_outline_json_is_valid_json`: open `latex_output/book_outline.json`; call `json.load()`; assert no exception
- [ ] Write `test_book_outline_has_six_chapters`: parse JSON; assert `len(data["chapters"]) == 6`
- [ ] Write `test_attention_complexity_png_exists`: assert `Path("latex_output/assets/attention_complexity.png").exists()`
- [ ] Write `test_sdp_attention_tex_exists`: assert `Path("latex_output/figures/sdp_attention.tex").exists()`
- [ ] Write `test_main_tex_contains_six_input_commands`: read `latex_output/main.tex`; count occurrences of `\\input{`; assert `== 6`
- [ ] Confirm `uv run pytest tests/test_integration.py` shows all tests skipped or collection error (not a test run crash)
- [ ] Run `uv run ruff check tests/test_integration.py` — confirm exits 0

---

## Phase 9: Implement `src/config.py`

> Gate: `uv run pytest tests/test_config.py` must currently exit non-zero before starting this phase.

- [ ] Create `src/config.py` with `from pydantic_settings import BaseSettings, SettingsConfigDict`
- [ ] Define `class Settings(BaseSettings)` with field `LLM_MODEL: str = "claude-sonnet-4-6"`
- [ ] Add field `ANTHROPIC_API_KEY: str` with no default (required field)
- [ ] Add field `PERPLEXITY_API_KEY: str` with no default (required field)
- [ ] Add field `MAX_AGENT_RETRIES: int = 3`
- [ ] Add field `PYTHON_RUNNER_TIMEOUT_S: int = 60`
- [ ] Add field `LUALATEX_BIN: str = "lualatex"`
- [ ] Add field `BIBER_BIN: str = "biber"`
- [ ] Add field `PANDOC_BIN: str = "pandoc"`
- [ ] Add field `OUTPUT_DIR: str = "latex_output"`
- [ ] Add field `ASSETS_DIR: str = "latex_output/assets"`
- [ ] Add field `MIN_PAGES: int = 15`
- [ ] Add `model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")` to `Settings`
- [ ] Add module-level `settings = Settings()` instantiation as the singleton
- [ ] Run `uv run pytest tests/test_config.py` — confirm exits 0 (all config tests green)
- [ ] Run `uv run ruff check src/config.py` — confirm exits 0
- [ ] Run `wc -l src/config.py` — confirm result ≤ 50 lines

---

## Phase 10: Implement `src/tools/latex_writer.py`

> Gate: `uv run pytest tests/test_latex_writer.py` must currently exit non-zero before starting this phase.

- [ ] Create `src/tools/latex_writer.py` with imports: `pathlib.Path`, `typing.Literal`, `pydantic.BaseModel`, `crewai_tools.BaseTool`, `src.config.settings`
- [ ] Define `class LatexWriterInput(BaseModel)` with field `path: str`
- [ ] Add field `content: str` to `LatexWriterInput`
- [ ] Add field `mode: Literal["write", "append"]` to `LatexWriterInput`
- [ ] Define `class LatexWriterTool(BaseTool)` with class attribute `name = "latex_writer"`
- [ ] Add `description` class attribute: one sentence describing the tool writes or appends LaTeX content to a file inside the output directory
- [ ] Set `args_schema = LatexWriterInput` on `LatexWriterTool`
- [ ] Implement `_validate_path(self, path: str) -> Path` method
- [ ] In `_validate_path`: resolve the path relative to `Path(settings.OUTPUT_DIR)`
- [ ] In `_validate_path`: call `.is_relative_to(Path(settings.OUTPUT_DIR).resolve())`; raise `ValueError` with a descriptive message if the check fails
- [ ] In `_validate_path`: return the validated resolved `Path` object
- [ ] Implement `_run(self, path: str, content: str, mode: str) -> str` method
- [ ] In `_run`: call `self._validate_path(path)` to obtain the safe resolved path
- [ ] In `_run`: call `resolved.parent.mkdir(parents=True, exist_ok=True)` to ensure directories exist
- [ ] In `_run` write branch (`mode == "write"`): open file with `open(resolved, "w", encoding="utf-8")` and write content
- [ ] In `_run` append branch (`mode == "append"`): open file with `open(resolved, "a", encoding="utf-8")` and write content
- [ ] In `_run`: return a confirmation string that includes the resolved file path
- [ ] Add module-level `latex_writer_tool = LatexWriterTool()` singleton instantiation
- [ ] Run `uv run pytest tests/test_latex_writer.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tools/latex_writer.py` — confirm exits 0
- [ ] Run `wc -l src/tools/latex_writer.py` — confirm result ≤ 85 lines

---

## Phase 10.5: Implement `src/tools/perplexity_search.py`

> Gate: `uv run pytest tests/test_perplexity_search.py` must currently exit non-zero before starting this phase.

- [ ] Create `src/tools/perplexity_search.py` with imports: `requests`, `pydantic.BaseModel`, `crewai_tools.BaseTool`, `src.config.settings`
- [ ] Define `class PerplexitySearchInput(BaseModel)` with field `query: str`
- [ ] Add field `max_results: int = 5` to `PerplexitySearchInput`
- [ ] Define `class PerplexitySearchTool(BaseTool)` with class attribute `name = "perplexity_search"`
- [ ] Add `description` class attribute explaining the tool queries Perplexity AI for academic research
- [ ] Set `args_schema = PerplexitySearchInput` on `PerplexitySearchTool`
- [ ] Implement `_run(self, query: str, max_results: int) -> str` method
- [ ] In `_run`: raise `ValueError` if `query` is empty or whitespace-only
- [ ] In `_run`: construct request payload with `model="sonar-pro"` and the query as a user message
- [ ] In `_run`: send `requests.post` to the Perplexity AI endpoint with `Authorization: Bearer {settings.PERPLEXITY_API_KEY}`
- [ ] In `_run`: raise `ValueError` for HTTP 4xx errors; re-raise `requests.HTTPError` for HTTP 429 (rate limit) so Manager Agent can retry
- [ ] In `_run`: extract and return the assistant message content as a plain string
- [ ] Add module-level `perplexity_search_tool = PerplexitySearchTool()` singleton instantiation
- [ ] Run `uv run pytest tests/test_perplexity_search.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tools/perplexity_search.py` — confirm exits 0
- [ ] Run `wc -l src/tools/perplexity_search.py` — confirm result ≤ 70 lines

---

## Phase 10.6: Implement `src/tools/markdown_converter.py`

> Gate: `uv run pytest tests/test_markdown_converter.py` must currently exit non-zero before starting this phase.

- [ ] Create `src/tools/markdown_converter.py` with imports: `subprocess`, `pathlib.Path`, `pydantic.BaseModel`, `crewai_tools.BaseTool`, `src.config.settings`
- [ ] Define `class MarkdownConverterInput(BaseModel)` with field `md_path: str`
- [ ] Add field `tex_path: str` to `MarkdownConverterInput`
- [ ] Define `class MarkdownConverterTool(BaseTool)` with class attribute `name = "markdown_converter"`
- [ ] Add `description` class attribute explaining the tool converts a Markdown file to LaTeX using pandoc
- [ ] Set `args_schema = MarkdownConverterInput` on `MarkdownConverterTool`
- [ ] Implement `_validate_path(self, path: str) -> Path` method (identical path-traversal guard as in `latex_writer.py`)
- [ ] Implement `_run(self, md_path: str, tex_path: str) -> str` method
- [ ] In `_run`: validate both `md_path` and `tex_path` using `_validate_path`
- [ ] In `_run`: call `subprocess.run([settings.PANDOC_BIN, "-f", "markdown", "-t", "latex", "-o", str(resolved_tex), str(resolved_md)], check=True)`
- [ ] In `_run`: if `subprocess.CalledProcessError` is raised, re-raise with a descriptive message containing the pandoc stderr output
- [ ] In `_run`: return a confirmation string including the resolved output `.tex` path
- [ ] Add module-level `markdown_converter_tool = MarkdownConverterTool()` singleton instantiation
- [ ] Run `uv run pytest tests/test_markdown_converter.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tools/markdown_converter.py` — confirm exits 0
- [ ] Run `wc -l src/tools/markdown_converter.py` — confirm result ≤ 60 lines

---

## Phase 11: Implement `src/tools/python_runner.py`

> Gate: `uv run pytest tests/test_python_runner.py` must currently exit non-zero before starting this phase.

- [ ] Create `src/tools/python_runner.py` with imports: `ast`, `subprocess`, `tempfile`, `pathlib.Path`, `pydantic.BaseModel`, `crewai_tools.BaseTool`, `src.config.settings`
- [ ] Define `ALLOWED_IMPORTS: frozenset` at module level containing `{"matplotlib", "numpy", "pathlib", "os"}`
- [ ] Add a comment on `ALLOWED_IMPORTS` explaining it is a security invariant, not a tuneable hyperparameter, and must not be moved to `.env`
- [ ] Define `class PythonRunnerInput(BaseModel)` with field `script: str`
- [ ] Define `class PythonRunnerTool(BaseTool)` with class attribute `name = "python_runner"`
- [ ] Add `description` class attribute to `PythonRunnerTool`
- [ ] Set `args_schema = PythonRunnerInput` on `PythonRunnerTool`
- [ ] Implement `_scan_imports(self, script: str) -> list[str]` method
- [ ] In `_scan_imports`: call `ast.parse(script)` to obtain the AST tree
- [ ] In `_scan_imports`: walk the tree; collect top-level names from all `ast.Import` nodes
- [ ] In `_scan_imports`: walk the tree; collect module names from all `ast.ImportFrom` nodes
- [ ] In `_scan_imports`: compute the set difference against `ALLOWED_IMPORTS`; return the disallowed names as a sorted list
- [ ] Implement `_run(self, script: str) -> str` method
- [ ] In `_run`: call `self._scan_imports(script)`; if the result is non-empty, raise `ValueError` listing the disallowed import names
- [ ] In `_run`: write the script to a `tempfile.NamedTemporaryFile` with suffix `".py"` and `delete=False`
- [ ] In `_run`: call `subprocess.run(["python3", tmpfile_path], capture_output=True, text=True, timeout=settings.PYTHON_RUNNER_TIMEOUT_S)`
- [ ] In `_run`: if `returncode != 0`, return the stderr string so the agent can inspect and retry
- [ ] In `_run`: if `returncode == 0`, return the stdout string
- [ ] In `_run`: catch `subprocess.TimeoutExpired` and re-raise it (let CrewAI handle retry)
- [ ] Add module-level `python_runner_tool = PythonRunnerTool()` singleton instantiation
- [ ] Run `uv run pytest tests/test_python_runner.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tools/python_runner.py` — confirm exits 0
- [ ] Run `wc -l src/tools/python_runner.py` — confirm result ≤ 95 lines
- [ ] If line count exceeds 95, extract `_scan_imports` logic into `src/tools/_import_scanner.py` and import from there

---

## Phase 12: Implement `src/tools/lualatex_runner.py`

> Gate: `uv run pytest tests/test_lualatex_runner.py` must currently exit non-zero before starting this phase.

- [ ] Create `src/tools/lualatex_runner.py` with imports: `subprocess`, `pathlib.Path`, `pydantic.BaseModel`, `crewai_tools.BaseTool`, `src.config.settings`
- [ ] Define `class CompilationError(Exception): pass`
- [ ] Define `class LualatexRunnerInput(BaseModel)` with field `tex_file: str`
- [ ] Add field `passes: int = 2` to `LualatexRunnerInput`
- [ ] Add field `run_biber: bool = True` to `LualatexRunnerInput`
- [ ] Define `class LualatexRunnerTool(BaseTool)` with class attribute `name = "lualatex_runner"`
- [ ] Add `description` class attribute to `LualatexRunnerTool`
- [ ] Set `args_schema = LualatexRunnerInput` on `LualatexRunnerTool`
- [ ] Implement `_build_lualatex_cmd(self, tex_file: str) -> list[str]` method
- [ ] In `_build_lualatex_cmd`: return `[settings.LUALATEX_BIN, "--interaction=nonstopmode", f"--output-directory={settings.OUTPUT_DIR}", tex_file]`
- [ ] Implement `_build_biber_cmd(self, stem: str) -> list[str]` method
- [ ] In `_build_biber_cmd`: return `[settings.BIBER_BIN, stem]`
- [ ] Implement `_parse_log(self, log_path: Path) -> list[str]` method
- [ ] In `_parse_log`: read the log file with `encoding="utf-8", errors="replace"`
- [ ] In `_parse_log`: filter and return only lines that begin with `"! "`
- [ ] Implement `_run(self, tex_file: str, passes: int, run_biber: bool) -> dict` method
- [ ] In `_run`: execute `subprocess.run(self._build_lualatex_cmd(tex_file), ...)` for pass 1
- [ ] In `_run`: if `run_biber` is True, execute `subprocess.run(self._build_biber_cmd(stem), ...)` between passes
- [ ] In `_run`: execute `subprocess.run(self._build_lualatex_cmd(tex_file), ...)` for pass 2
- [ ] In `_run`: after the final lualatex pass, derive the log path from `Path(settings.OUTPUT_DIR) / (Path(tex_file).stem + ".log")`
- [ ] In `_run`: call `self._parse_log(log_path)`; if the result list is non-empty, raise `CompilationError(errors_list)`
- [ ] In `_run`: derive pdf_path from `Path(settings.OUTPUT_DIR) / (Path(tex_file).stem + ".pdf")`
- [ ] In `_run`: return `{"success": True, "pdf_path": str(pdf_path), "log_tail": ""}` on success
- [ ] Add module-level `lualatex_runner_tool = LualatexRunnerTool()` singleton instantiation
- [ ] Run `uv run pytest tests/test_lualatex_runner.py` — confirm exits 0 (non-skipped tests pass)
- [ ] Run `uv run ruff check src/tools/lualatex_runner.py` — confirm exits 0
- [ ] Run `wc -l src/tools/lualatex_runner.py` — confirm result ≤ 100 lines
- [ ] If line count exceeds 100, extract `_parse_log` into `src/tools/_log_parser.py` and import from there

---

## Phase 13: Implement `src/agents/manager_agent.py`

- [ ] Create `src/agents/manager_agent.py` with imports: `crewai.Agent`, `src.config.settings`
- [ ] Define function `build_manager_agent(backstory: str) -> Agent`
- [ ] In function: construct `Agent` with `role="Project Manager"`
- [ ] Set `goal` to: orchestrate all sub-agents to produce a compiled Hebrew academic PDF
- [ ] Set `backstory=backstory`, `allow_delegation=True`, `llm=settings.LLM_MODEL`, `max_retry_limit=settings.MAX_AGENT_RETRIES`, `verbose=True`
- [ ] Set `tools=[]` (manager delegates; it does not call tools directly)
- [ ] Return the constructed `Agent`
- [ ] Run `uv run ruff check src/agents/manager_agent.py` — exits 0
- [ ] Run `wc -l src/agents/manager_agent.py` — confirm ≤ 30 lines

---

## Phase 13 continued: Implement `src/agents/researcher_agent.py`

- [ ] Create `src/agents/researcher_agent.py` with imports: `crewai.Agent`, `src.config.settings`, `src.tools.perplexity_search.perplexity_search_tool`
- [ ] Define function `build_researcher_agent(backstory: str) -> Agent`
- [ ] In function: construct `Agent` with `role="Academic Researcher"`
- [ ] Set `goal` to: use Perplexity AI to gather academic sources on Transformer architectures for the outline agent
- [ ] Set `backstory=backstory`, `tools=[perplexity_search_tool]`, `llm=settings.LLM_MODEL`, `max_retry_limit=settings.MAX_AGENT_RETRIES`, `verbose=True`
- [ ] Return the constructed `Agent`
- [ ] Run `uv run ruff check src/agents/researcher_agent.py` — exits 0
- [ ] Run `wc -l src/agents/researcher_agent.py` — confirm ≤ 30 lines

---

## Phase 13 continued: Implement `src/agents/outline_agent.py`

- [ ] Create `src/agents/outline_agent.py` with imports: `crewai.Agent`, `src.config.settings`, `src.tools.latex_writer.latex_writer_tool`
- [ ] Define function `build_outline_agent(backstory: str) -> Agent`
- [ ] In function: construct `Agent` with `role="Academic Outline Architect"`
- [ ] Set `goal` to a one-sentence description: produce a structured 6-chapter book outline as a valid JSON file
- [ ] Set `backstory=backstory` (value injected from SKILL.md by crew.py)
- [ ] Set `tools=[latex_writer_tool]`
- [ ] Set `llm=settings.LLM_MODEL` and `max_retry_limit=settings.MAX_AGENT_RETRIES`
- [ ] Set `verbose=True`
- [ ] Return the constructed `Agent`
- [ ] Run `uv run ruff check src/agents/outline_agent.py` — exits 0
- [ ] Run `wc -l src/agents/outline_agent.py` — confirm ≤ 30 lines

---

## Phase 13 continued: Implement `src/agents/content_agent.py`

- [ ] Create `src/agents/content_agent.py` with imports: `crewai.Agent`, `src.config.settings`, `src.tools.latex_writer.latex_writer_tool`, `src.tools.markdown_converter.markdown_converter_tool`
- [ ] Define function `build_content_agent(backstory: str) -> Agent`
- [ ] Set `role="Hebrew Academic Writer"`
- [ ] Set `goal` describing production of Hebrew-language chapter files via Markdown-first workflow (write `.md`, convert to `.tex`)
- [ ] Set `backstory=backstory`, `tools=[latex_writer_tool, markdown_converter_tool]`, `llm=settings.LLM_MODEL`, `max_retry_limit=settings.MAX_AGENT_RETRIES`, `verbose=True`
- [ ] Return the constructed `Agent`
- [ ] Run `uv run ruff check src/agents/content_agent.py` — exits 0
- [ ] Run `wc -l src/agents/content_agent.py` — confirm ≤ 30 lines

---

## Phase 13 continued: Implement `src/agents/bidi_agent.py`

- [ ] Create `src/agents/bidi_agent.py` with imports: `crewai.Agent`, `src.config.settings`, `src.tools.latex_writer.latex_writer_tool`
- [ ] Define function `build_bidi_agent(backstory: str) -> Agent`
- [ ] Set `role="LaTeX BiDi Typesetting Specialist"`
- [ ] Set `goal` describing validation and active enforcement of BiDi correctness across all 6 chapter files
- [ ] Set `backstory=backstory`, `tools=[latex_writer_tool]`, `llm=settings.LLM_MODEL`, `max_retry_limit=settings.MAX_AGENT_RETRIES`, `verbose=True`
- [ ] Return the constructed `Agent`
- [ ] Run `uv run ruff check src/agents/bidi_agent.py` — exits 0
- [ ] Run `wc -l src/agents/bidi_agent.py` — confirm ≤ 30 lines

---

## Phase 13 continued: Implement `src/agents/figure_agent.py`

- [ ] Create `src/agents/figure_agent.py` with imports: `crewai.Agent`, `src.config.settings`, `src.tools.python_runner.python_runner_tool`, `src.tools.latex_writer.latex_writer_tool`
- [ ] Define function `build_figure_agent(backstory: str) -> Agent`
- [ ] Set `role="Scientific Figure Generator"`
- [ ] Set `goal` describing production of the attention complexity PNG and the TikZ SDP diagram
- [ ] Set `tools=[python_runner_tool, latex_writer_tool]`
- [ ] Set `backstory=backstory`, `llm=settings.LLM_MODEL`, `max_retry_limit=settings.MAX_AGENT_RETRIES`, `verbose=True`
- [ ] Return the constructed `Agent`
- [ ] Run `uv run ruff check src/agents/figure_agent.py` — exits 0
- [ ] Run `wc -l src/agents/figure_agent.py` — confirm ≤ 30 lines

---

## Phase 13 continued: Implement `src/agents/compiler_agent.py`

- [ ] Create `src/agents/compiler_agent.py` with imports: `crewai.Agent`, `src.config.settings`, `src.tools.lualatex_runner.lualatex_runner_tool`
- [ ] Define function `build_compiler_agent(backstory: str) -> Agent`
- [ ] Set `role="LaTeX Build Engineer"`
- [ ] Set `goal` describing assembly of `main.tex` preamble and two-pass lualatex compilation to PDF
- [ ] Set `tools=[lualatex_runner_tool]`
- [ ] Set `backstory=backstory`, `llm=settings.LLM_MODEL`, `max_retry_limit=settings.MAX_AGENT_RETRIES`, `verbose=True`
- [ ] Return the constructed `Agent`
- [ ] Run `uv run ruff check src/agents/compiler_agent.py` — exits 0
- [ ] Run `wc -l src/agents/compiler_agent.py` — confirm ≤ 30 lines

---

## Phase 14: Implement `src/tasks/research_task.py`

- [ ] Create `src/tasks/research_task.py` with imports: `crewai.Task`, `crewai.Agent`
- [ ] Define function `build_research_task(agent: Agent) -> Task`
- [ ] Write `description` string: instruct the agent to use `perplexity_search_tool` to research at least 6 academic sources on Transformer architectures, attention mechanisms, and Hebrew NLP
- [ ] In description: specify the required output format — a Markdown block with one entry per source containing: citation key, authors, year, title, venue, and a 2-sentence summary
- [ ] In description: specify that citation keys must follow the pattern `author_year_keyword` (e.g., `vaswani2017attention`) to match the expected `refs.bib` keys
- [ ] Set `expected_output = "Structured research notes with at least 6 citation-ready academic sources"`
- [ ] Set `agent=agent` on the Task
- [ ] Set `context=[]` (research task has no upstream dependencies)
- [ ] Run `uv run ruff check src/tasks/research_task.py` — exits 0
- [ ] Run `wc -l src/tasks/research_task.py` — confirm ≤ 40 lines

---

## Phase 14 continued: Implement `src/tasks/outline_task.py`

- [ ] Create `src/tasks/outline_task.py` with imports: `crewai.Task`, `crewai.Agent`
- [ ] Define function `build_outline_task(agent: Agent) -> Task`
- [ ] Write `description` string: instruct the agent to use `latex_writer_tool` in write mode to produce `latex_output/book_outline.json`
- [ ] In description: embed the full required JSON schema (fields `title`, `subtitle`, `chapters` array with `number`, `hebrew_title`, `english_title`, `page_budget`, `sections`)
- [ ] In description: state explicitly that all chapter `page_budget` values must sum to 15
- [ ] In description: state that the JSON must be valid (no trailing commas, no comments)
- [ ] In description: state that the file path must be exactly `latex_output/book_outline.json`
- [ ] Set `expected_output = "Valid JSON file at latex_output/book_outline.json with 6 chapters"`
- [ ] Set `agent=agent` on the Task
- [ ] Run `uv run ruff check src/tasks/outline_task.py` — exits 0
- [ ] Run `wc -l src/tasks/outline_task.py` — confirm ≤ 40 lines

---

## Phase 14 continued: Implement `src/tasks/content_task.py`

- [ ] Create `src/tasks/content_task.py` with imports: `crewai.Task`, `crewai.Agent`
- [ ] Define module-level `CHAPTER_SPECS: list[tuple[int, str, str, int]]` constant with 6 entries
- [ ] Add entry 1: `(1, "מבוא", "Introduction to Transformers", 2)`
- [ ] Add entry 2: `(2, "ארכיטקטורה", "Transformer Architecture Deep Dive", 3)`
- [ ] Add entry 3: `(3, "דו-כיווניות", "BiDi Text in Academic Publishing", 2)` — this is the BiDi showcase chapter
- [ ] Add entry 4: `(4, "יישומים", "Applications and Fine-Tuning", 3)`
- [ ] Add entry 5: `(5, "הערכה", "Evaluation Methodologies", 2)`
- [ ] Add entry 6: `(6, "סיכום", "Conclusion and Future Work", 3)`
- [ ] Add an `assert sum(pages for _, _, _, pages in CHAPTER_SPECS) == 15` guard after the definition
- [ ] Define function `build_content_tasks(agent: Agent, outline_task: Task) -> list[Task]`
- [ ] In function: iterate over `CHAPTER_SPECS` unpacking `ch_num, heb_title, eng_title, pages`
- [ ] For each chapter: construct a `Task` with a `description` parameterized with `ch_num`, `heb_title`, `eng_title`, `pages`
- [ ] In each description: instruct the agent to write `latex_output/chapters/ch{ch_num}.tex` using `latex_writer_tool`
- [ ] In each description: specify file must start with `\chapter{heb_title}` and must NOT contain `\begin{document}`
- [ ] In each description: specify that inline math uses `\(` and `\)`, display math uses `\begin{equation}`
- [ ] In each description: state the page budget target of `pages` pages
- [ ] Set `context=[outline_task]` on each content task
- [ ] Set `expected_output` for each task referencing the chapter file path
- [ ] Set `agent=agent` on each task
- [ ] Append each task to a results list and return it
- [ ] Run `uv run ruff check src/tasks/content_task.py` — exits 0
- [ ] Run `wc -l src/tasks/content_task.py` — confirm ≤ 65 lines
- [ ] If count exceeds 65, extract `CHAPTER_SPECS` to `src/tasks/_chapter_specs.py` and import

---

## Phase 14 continued: Implement `src/tasks/bidi_task.py`

- [ ] Create `src/tasks/bidi_task.py` with imports: `crewai.Task`, `crewai.Agent`
- [ ] Define function `build_bidi_task(agent: Agent, content_tasks: list[Task]) -> Task`
- [ ] Write `description` string: instruct the agent to read and validate all six chapter files in `latex_output/chapters/`
- [ ] In description: mandate that `ch3.tex` must contain (1) an RTL paragraph with inline `\textenglish{}`, (2) a `\begin{equation}` environment, (3) a `\begin{LTR}...\end{LTR}` block — and to add any that are missing
- [ ] In description: instruct the agent to overwrite each chapter file in-place via `latex_writer_tool` if corrections are needed
- [ ] In description: include the 5-item validation checklist from the lualatex-bidi SKILL.md
- [ ] Set `context=content_tasks` on the task
- [ ] Set `expected_output = "All six chapters updated in-place; ch3.tex contains all three mandatory BiDi constructs"`
- [ ] Set `agent=agent` on the task
- [ ] Run `uv run ruff check src/tasks/bidi_task.py` — exits 0
- [ ] Run `wc -l src/tasks/bidi_task.py` — confirm ≤ 40 lines

---

## Phase 14 continued: Implement `src/tasks/figure_task.py`

- [ ] Create `src/tasks/figure_task.py` with imports: `crewai.Task`, `crewai.Agent`
- [ ] Define function `build_figure_task(agent: Agent, outline_task: Task) -> Task`
- [ ] Write `description` string: instruct the agent to write and execute a Python script via `python_runner_tool`
- [ ] In description: specify the script must save to `latex_output/assets/attention_complexity.png` at 300 dpi
- [ ] In description: specify three required curves — O(n²) standard attention, O(n log n) linear attention, O(n) recurrent
- [ ] In description: specify x-axis label "Sequence Length (n)" and y-axis label "Complexity" with a legend
- [ ] In description: instruct the agent to also write a TikZ block to `latex_output/figures/sdp_attention.tex` via `latex_writer_tool`
- [ ] In description: specify the TikZ block must represent scaled dot-product attention with Q, K, V node labels
- [ ] Set `context=[outline_task]` on the task
- [ ] Set `expected_output = "attention_complexity.png and sdp_attention.tex both exist in their respective output directories"`
- [ ] Set `agent=agent` on the task
- [ ] Run `uv run ruff check src/tasks/figure_task.py` — exits 0
- [ ] Run `wc -l src/tasks/figure_task.py` — confirm ≤ 45 lines

---

## Phase 14 continued: Implement `src/tasks/compile_task.py`

- [ ] Create `src/tasks/compile_task.py` with imports: `crewai.Task`, `crewai.Agent`
- [ ] Define function `build_compile_task(agent: Agent, bidi_task: Task, figure_task: Task) -> Task`
- [ ] Write `description` string: instruct agent to first write `latex_output/main.tex` via `latex_writer_tool`
- [ ] In description: specify document class `\documentclass[17pt,a4paper]{extarticle}`
- [ ] In description: specify the 10 required packages in preamble: `fontspec`, `polyglossia`, `biblatex`, `geometry`, `graphicx`, `amsmath`, `hyperref`, `tikz`, `booktabs`, `xcolor`
- [ ] In description: specify `fontspec` Hebrew font fallback chain: `David CLM` → `Frank Ruehl CLM` → `Noto Serif Hebrew`
- [ ] In description: specify `\setmainlanguage{hebrew}` and `\setotherlanguage{english}` from polyglossia
- [ ] In description: specify `\addbibresource{refs.bib}` in the preamble
- [ ] In description: specify the exact 6 `\input{}` calls in order from `chapters/ch1` to `chapters/ch6`
- [ ] In description: specify `\printbibliography` after the last `\input{}` call and before `\end{document}`
- [ ] In description: instruct agent to call `lualatex_runner_tool` with `tex_file="latex_output/main.tex"` and `passes=2`
- [ ] Set `context=[bidi_task, figure_task]` on the task
- [ ] Set `expected_output = "latex_output/main.pdf exists; two-pass lualatex exits 0"` on the task
- [ ] Set `agent=agent` on the task
- [ ] Run `uv run ruff check src/tasks/compile_task.py` — exits 0
- [ ] Run `wc -l src/tasks/compile_task.py` — confirm ≤ 45 lines

---

## Phase 15: Implement `src/crew.py`

> Gate: `uv run pytest tests/test_crew.py` must currently exit non-zero before starting this phase.

- [ ] Create `src/crew.py` with imports: `pathlib.Path`, `crewai.Crew`, `crewai.Process`
- [ ] Import `build_manager_agent` from `src.agents.manager_agent`
- [ ] Import `build_researcher_agent` from `src.agents.researcher_agent`
- [ ] Import `build_outline_agent` from `src.agents.outline_agent`
- [ ] Import `build_content_agent` from `src.agents.content_agent`
- [ ] Import `build_bidi_agent` from `src.agents.bidi_agent`
- [ ] Import `build_figure_agent` from `src.agents.figure_agent`
- [ ] Import `build_compiler_agent` from `src.agents.compiler_agent`
- [ ] Import all six task builder functions from their respective `src.tasks.*` modules (including `build_research_task`)
- [ ] Define module-level function `_load_skill(name: str) -> str`
- [ ] In `_load_skill`: construct `path = Path("skills") / name / "SKILL.md"`
- [ ] In `_load_skill`: return `path.read_text(encoding="utf-8")` — this is the only place SKILL.md files are read
- [ ] Define `class PublisherCrew`
- [ ] Implement `__init__(self)`: load all 7 skills via `_load_skill` — if any file is missing, `FileNotFoundError` propagates immediately
- [ ] In `__init__`: construct all 7 agents by calling their builder functions, passing the corresponding skill string as `backstory`
- [ ] In `__init__`: construct `self.research_task` via `build_research_task(self.researcher_agent)`
- [ ] In `__init__`: construct `self.outline_task` via `build_outline_task(self.outline_agent)`
- [ ] In `__init__`: construct `self.content_tasks` via `build_content_tasks(self.content_agent, self.outline_task)`
- [ ] In `__init__`: construct `self.figure_task` via `build_figure_task(self.figure_agent, self.outline_task)`
- [ ] In `__init__`: construct `self.bidi_task` via `build_bidi_task(self.bidi_agent, self.content_tasks)`
- [ ] In `__init__`: construct `self.compile_task` via `build_compile_task(self.compiler_agent, self.bidi_task, self.figure_task)`
- [ ] Implement `kickoff(self) -> str` method
- [ ] In `kickoff`: assemble `tasks = [self.research_task, self.outline_task, *self.content_tasks, self.figure_task, self.bidi_task, self.compile_task]`
- [ ] In `kickoff`: construct `Crew(manager_agent=self.manager_agent, agents=[self.researcher_agent, self.outline_agent, self.content_agent, self.bidi_agent, self.figure_agent, self.compiler_agent], tasks=tasks, process=Process.hierarchical, verbose=True)`
- [ ] In `kickoff`: return `crew.kickoff()`
- [ ] Run `uv run pytest tests/test_crew.py` — confirm exits 0 (all crew tests green)
- [ ] Run `uv run ruff check src/crew.py` — confirm exits 0
- [ ] Run `wc -l src/crew.py` — confirm ≤ 100 lines

---

## Phase 16: Implement `main.py`

- [ ] Open `main.py` and verify it is currently a stub or empty file
- [ ] Add `from src.crew import PublisherCrew` as the sole import
- [ ] Add `if __name__ == "__main__":` guard
- [ ] Inside guard: `crew = PublisherCrew()`
- [ ] Inside guard: `result = crew.kickoff()`
- [ ] Inside guard: `print(result)`
- [ ] Run `uv run ruff check main.py` — confirm exits 0
- [ ] Run `wc -l main.py` — confirm ≤ 10 lines
- [ ] Run `uv run pytest --cov=src --cov-fail-under=80` — confirm exits 0 with coverage ≥ 80%

---

## Phase 17: Directory Scaffolding & `latex_output/refs.bib`

- [ ] Confirm `latex_output/` directory exists and contains `.gitkeep`
- [ ] Confirm `latex_output/assets/` directory exists and contains `.gitkeep`
- [ ] Confirm `latex_output/chapters/` directory exists and contains `.gitkeep`
- [ ] Confirm `latex_output/figures/` directory exists and contains `.gitkeep`
- [ ] Create `latex_output/refs.bib` (this file is hand-authored and committed to the repository)
- [ ] Add BibTeX entry 1: `@article{vaswani2017attention}` — Vaswani et al. 2017 "Attention is All You Need"
- [ ] Add BibTeX entry 2: `@article{devlin2019bert}` — Devlin et al. 2019 "BERT: Pre-training of Deep Bidirectional Transformers"
- [ ] Add BibTeX entry 3: `@article{brown2020language}` — Brown et al. 2020 "Language Models are Few-Shot Learners"
- [ ] Add BibTeX entry 4: `@article{radford2019language}` — Radford et al. 2019 "Language Models are Unsupervised Multitask Learners"
- [ ] Add BibTeX entry 5: `@article{touvron2023llama}` — Touvron et al. 2023 "LLaMA: Open and Efficient Foundation Language Models"
- [ ] Add BibTeX entry 6: `@article{clark2020electra}` — Clark et al. 2020 "ELECTRA: Pre-training Text Encoders as Discriminators"
- [ ] Verify `latex_output/refs.bib` contains exactly 6 `@` entry declarations
- [ ] Verify each BibTeX entry has `author`, `title`, `year`, and `journal` or `booktitle` fields
- [ ] Verify BibTeX is syntactically valid: balanced braces, comma after each field except the last
- [ ] Verify no BibTeX key is duplicated in `refs.bib`
- [ ] Verify citation keys in `refs.bib` match the keys expected to appear in chapter `\cite{}` commands

---

## Phase 18: Post-Run LaTeX Content Validation

- [ ] After running the pipeline, verify `latex_output/book_outline.json` exists
- [ ] Verify `book_outline.json` is valid JSON: run `python -m json.tool latex_output/book_outline.json` — exits 0
- [ ] Verify `book_outline.json` has exactly 6 entries in the `chapters` array
- [ ] Verify each chapter object in `book_outline.json` has a `hebrew_title` field that is non-empty
- [ ] Verify each chapter object in `book_outline.json` has a `page_budget` field that is a positive integer
- [ ] Verify the sum of all `page_budget` values in `book_outline.json` equals 15
- [ ] Verify `latex_output/chapters/ch1.tex` exists and is non-empty
- [ ] Verify `ch1.tex` begins with `\chapter{` on the first non-blank line
- [ ] Verify `ch1.tex` does NOT contain the string `\begin{document}`
- [ ] Verify `latex_output/chapters/ch2.tex` exists and is non-empty
- [ ] Verify `latex_output/chapters/ch3.tex` exists and is non-empty
- [ ] Verify `ch3.tex` contains `\textenglish{` at least once
- [ ] Verify `ch3.tex` contains `\begin{equation}` at least once
- [ ] Verify `ch3.tex` contains `\begin{LTR}` at least once
- [ ] Verify `latex_output/chapters/ch4.tex`, `ch5.tex`, `ch6.tex` all exist and are non-empty
- [ ] Verify `latex_output/assets/attention_complexity.png` exists
- [ ] Verify PNG file size is greater than 10 KB (not a placeholder empty file)
- [ ] Verify `latex_output/figures/sdp_attention.tex` exists and is non-empty
- [ ] Verify `sdp_attention.tex` contains `\begin{tikzpicture}` and `\end{tikzpicture}`
- [ ] Verify `latex_output/main.tex` exists and is non-empty
- [ ] Verify `main.tex` contains `\documentclass`
- [ ] Verify `main.tex` contains `\usepackage{fontspec}`
- [ ] Verify `main.tex` contains `\usepackage{polyglossia}` or the polyglossia load directive
- [ ] Verify `main.tex` contains `\setmainlanguage{hebrew}`
- [ ] Verify `main.tex` contains exactly 6 occurrences of `\input{`
- [ ] Verify `main.tex` contains `\addbibresource{refs.bib}`
- [ ] Verify `main.tex` contains `\printbibliography`
- [ ] Verify `latex_output/main.pdf` exists
- [ ] Verify `main.pdf` file size is greater than 100 KB

---

## Phase 19: Integration Run & Slow Test Execution

- [ ] Confirm `ANTHROPIC_API_KEY` is set in the shell environment (non-empty)
- [ ] Confirm `lualatex` binary is available: `which lualatex` exits 0
- [ ] Confirm at least one Hebrew font is available: `fc-list | grep -iE "David CLM|Frank Ruehl|Noto Serif Hebrew"` returns at least one match
- [ ] Run `uv run python main.py` and monitor console output for Python exceptions
- [ ] Confirm `main.py` run completes without raising an unhandled exception
- [ ] Confirm `latex_output/main.pdf` exists immediately after `main.py` run
- [ ] Run `uv run pytest -m slow tests/test_integration.py -v` — confirm exits 0
- [ ] Confirm test `test_full_pipeline_produces_pdf` passes
- [ ] Confirm test `test_pdf_has_minimum_fifteen_pages` passes
- [ ] Confirm test `test_all_six_chapter_files_exist` passes
- [ ] Confirm test `test_book_outline_json_is_valid_json` passes
- [ ] Confirm test `test_book_outline_has_six_chapters` passes
- [ ] Confirm test `test_attention_complexity_png_exists` passes
- [ ] Confirm test `test_sdp_attention_tex_exists` passes
- [ ] Confirm test `test_main_tex_contains_six_input_commands` passes
- [ ] Run `pdfinfo latex_output/main.pdf` and assert the `Pages:` field shows a value ≥ 15
- [ ] If page count is < 15: identify which chapters produced fewer pages than their `page_budget`; re-run affected content tasks with more explicit page guidance
- [ ] After any page-budget correction, re-run `uv run pytest -m slow` to confirm all slow tests still pass

---

## Phase 20: Continuous Ruff Linting Gates

- [ ] Run `uv run ruff check src/config.py` — confirm exits 0
- [ ] Run `uv run ruff check src/crew.py` — confirm exits 0
- [ ] Run `uv run ruff check src/agents/manager_agent.py` — confirm exits 0
- [ ] Run `uv run ruff check src/agents/researcher_agent.py` — confirm exits 0
- [ ] Run `uv run ruff check src/agents/outline_agent.py` — confirm exits 0
- [ ] Run `uv run ruff check src/agents/content_agent.py` — confirm exits 0
- [ ] Run `uv run ruff check src/agents/bidi_agent.py` — confirm exits 0
- [ ] Run `uv run ruff check src/agents/figure_agent.py` — confirm exits 0
- [ ] Run `uv run ruff check src/agents/compiler_agent.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tasks/research_task.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tasks/outline_task.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tasks/content_task.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tasks/bidi_task.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tasks/figure_task.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tasks/compile_task.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tools/latex_writer.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tools/python_runner.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tools/lualatex_runner.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tools/perplexity_search.py` — confirm exits 0
- [ ] Run `uv run ruff check src/tools/markdown_converter.py` — confirm exits 0
- [ ] Run `uv run ruff check tests/conftest.py` — confirm exits 0
- [ ] Run `uv run ruff check tests/test_config.py` — confirm exits 0
- [ ] Run `uv run ruff check tests/test_latex_writer.py` — confirm exits 0
- [ ] Run `uv run ruff check tests/test_python_runner.py` — confirm exits 0
- [ ] Run `uv run ruff check tests/test_lualatex_runner.py` — confirm exits 0
- [ ] Run `uv run ruff check tests/test_perplexity_search.py` — confirm exits 0
- [ ] Run `uv run ruff check tests/test_markdown_converter.py` — confirm exits 0
- [ ] Run `uv run ruff check tests/test_crew.py` — confirm exits 0
- [ ] Run `uv run ruff check tests/test_integration.py` — confirm exits 0
- [ ] Run `uv run ruff check main.py` — confirm exits 0
- [ ] Run `uv run ruff check .` (whole repository) — confirm exits 0 with zero violations

---

## Phase 21: Karpathy Principles Verification

### Think Before Coding
- [ ] Verify every `src/` module corresponds to a failing test that existed before it was implemented
- [ ] Verify that no `src/` file was created without a corresponding checked-off task in this TODO
- [ ] Verify `git log --oneline` shows test commits preceding implementation commits for each module pair

### Simplicity First
- [ ] Grep `src/` for functions exceeding 20 lines; flag any found for refactor consideration
- [ ] Verify `src/crew.py` contains zero LaTeX-specific string literals, zero Hebrew characters, and zero matplotlib references
- [ ] Verify each agent module contains exactly one function and zero helper logic
- [ ] Verify no abstract base class, protocol, or decorator was introduced beyond what CrewAI requires
- [ ] Verify `CHAPTER_SPECS` is the only domain-structural constant defined outside `src/config.py`
- [ ] Verify `ALLOWED_IMPORTS` has a comment explaining why it belongs in code, not in `.env`
- [ ] Verify no `try/except` block catches the bare `Exception` type (each handler targets a specific exception class)
- [ ] Verify no `**kwargs` or `*args` appear in any function signature in `src/` beyond framework-required overrides

### Surgical Changes
- [ ] Verify no commit mixes a functional change with a rename, reformat, or unrelated cleanup
- [ ] Verify no import was added to a module without a failing test that required it
- [ ] Verify every `__init__.py` in `src/` is empty (zero bytes or only a newline)
- [ ] Grep all `.py` files for `client.messages.create` — assert zero matches (no raw Anthropic SDK calls)
- [ ] Verify `src/config.py` imports nothing from `src/agents/`, `src/tasks/`, or `src/tools/`
- [ ] Verify `src/tools/` modules import nothing from `src/agents/` or `src/tasks/`
- [ ] Verify `src/tasks/` modules import nothing from `src/agents/`

### Goal-Driven Execution
- [ ] Verify every function in `src/` can be traced to a specific phase in this TODO or a PRD section
- [ ] Verify no `.py` file in `src/` contains a `# TODO` or `# FIXME` inline comment
- [ ] Verify no `print()` call exists in any `src/` file (CrewAI `verbose=True` handles logging)
- [ ] Verify no `if DEBUG:` or feature-flag conditional exists in any `src/` file
- [ ] Verify no commented-out code blocks exist in any `src/` file

---

## Phase 22: Line Budget Enforcement (Final Verification)

- [ ] Run `wc -l src/config.py` — assert ≤ 50 lines
- [ ] Run `wc -l src/crew.py` — assert ≤ 100 lines
- [ ] Run `wc -l src/agents/manager_agent.py` — assert ≤ 30 lines
- [ ] Run `wc -l src/agents/researcher_agent.py` — assert ≤ 30 lines
- [ ] Run `wc -l src/agents/outline_agent.py` — assert ≤ 30 lines
- [ ] Run `wc -l src/agents/content_agent.py` — assert ≤ 30 lines
- [ ] Run `wc -l src/agents/bidi_agent.py` — assert ≤ 30 lines
- [ ] Run `wc -l src/agents/figure_agent.py` — assert ≤ 30 lines
- [ ] Run `wc -l src/agents/compiler_agent.py` — assert ≤ 30 lines
- [ ] Run `wc -l src/tasks/research_task.py` — assert ≤ 40 lines
- [ ] Run `wc -l src/tasks/outline_task.py` — assert ≤ 40 lines
- [ ] Run `wc -l src/tasks/content_task.py` — assert ≤ 65 lines
- [ ] Run `wc -l src/tasks/bidi_task.py` — assert ≤ 40 lines
- [ ] Run `wc -l src/tasks/figure_task.py` — assert ≤ 45 lines
- [ ] Run `wc -l src/tasks/compile_task.py` — assert ≤ 45 lines
- [ ] Run `wc -l src/tools/latex_writer.py` — assert ≤ 85 lines
- [ ] Run `wc -l src/tools/python_runner.py` — assert ≤ 95 lines
- [ ] Run `wc -l src/tools/lualatex_runner.py` — assert ≤ 100 lines
- [ ] Run `wc -l src/tools/perplexity_search.py` — assert ≤ 70 lines
- [ ] Run `wc -l src/tools/markdown_converter.py` — assert ≤ 60 lines
- [ ] Run `find src/ -name "*.py" -exec wc -l {} +` — confirm no single file exceeds 150 lines
- [ ] If any file is between 120 and 150 lines, execute a pre-emptive extraction before the hard limit is breached

---

## Phase 23: Final Acceptance Criteria

- [ ] Run `uv run ruff check .` — exits 0 with zero violations
- [ ] Run `uv run pytest --cov=src --cov-fail-under=80` — exits 0 with coverage ≥ 80%
- [ ] Run `uv run pytest -m slow` — exits 0 (all integration tests pass)
- [ ] Confirm `latex_output/main.pdf` exists on disk
- [ ] Confirm PDF page count ≥ 15 as reported by `pdfinfo`
- [ ] Confirm `main.tex` preamble contains all 10 required packages
- [ ] Confirm all 6 chapter `.tex` files are present and non-empty
- [ ] Confirm `ch3.tex` contains all three mandatory BiDi constructs
- [ ] Confirm `latex_output/assets/attention_complexity.png` exists with the three required curves
- [ ] Confirm `latex_output/figures/sdp_attention.tex` contains a TikZ diagram with Q, K, V nodes
- [ ] Confirm `latex_output/refs.bib` contains exactly 6 valid BibTeX entries
- [ ] Confirm no `.py` file in `src/` exceeds 150 lines
- [ ] Confirm no hardcoded model names, token budgets, or path literals appear in any `.py` file outside `src/config.py` (except `ALLOWED_IMPORTS` and `CHAPTER_SPECS`)
- [ ] Confirm all 7 SKILL.md files exist, are non-empty, and are readable by `_load_skill()`
- [ ] Confirm `main.tex` was produced via the biber pipeline (lualatex → biber → lualatex)
- [ ] Run `git status` — confirm `.env` is not staged and no secrets are present in tracked files
- [ ] Confirm `latex_output/refs.bib` is committed to the repository
- [ ] Tag the release commit as `v1.0.0` after all acceptance criteria above are checked off
