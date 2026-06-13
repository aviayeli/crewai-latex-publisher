# QA Sweep Report — Mass-Produced Articles

**Date:** 2026-06-12  
**Scope:** 4 articles in `results/`  
**Method:** Automated PyMuPDF + LaTeX-log analysis (`tests/test_qa_sweep_mass_articles.py`)  
**Result:** 6 FAILED · 78 PASSED · 3 xfailed (informational) · 1 xpassed

---

## Test Run Summary

```
FAILED test_headers_present[1_sine_wave]
FAILED test_headers_present[2_security]
FAILED test_headers_present[3_xlstm]
FAILED test_headers_present[4_orchestration]
FAILED test_all_cite_keys_in_bib[2_security]
FAILED test_no_missing_biblatex_entry_in_log[2_security]
```

---

## Comparative Rubric Table

| Criterion | 1_sine_wave | 2_security | 3_xlstm | 4_orchestration |
|-----------|:-----------:|:----------:|:-------:|:---------------:|
| **Page count ≥ 15** | ✅ 15 pp | ✅ 15 pp | ✅ 15 pp | ✅ 15 pp |
| **Running Headers** | ⚠️ 3/15 pages | ⚠️ 2/15 pages | ⚠️ 2/15 pages | ⚠️ 2/15 pages |
| **Footer (page number)** | ✅ 14/15 pages | ✅ 14/15 pages | ✅ 14/15 pages | ✅ 14/15 pages |
| **plain pagestyle override** | ✅ Present | ✅ Present | ✅ Present | ✅ Present |
| **BiDi — `\thepage` wrapped** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **BiDi — page numbers decimal** | ✅ Clean | ✅ Clean | ✅ Clean | ✅ Clean |
| **BiDi — section numbers LTR** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Tables present** | ✅ 2 tables | ✅ 2 tables | ✅ 3 tables | ✅ 3 tables |
| **Display math environments** | ✅ 6 | ✅ 3 | ✅ 6 | ✅ 5 |
| **Python graphs embedded** | ✅ 2 PNGs | ✅ 2 PNGs | ✅ 2 PNGs | ✅ 2 PNGs |
| **Image count in PDF** | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 |
| **All `\cite{}` keys in refs.bib** | ✅ Clean | ❌ 1 missing | ✅ Clean | ✅ Clean |
| **No undefined citation (log)** | ✅ Clean | ❌ biblatex warns | ✅ Clean | ✅ Clean |
| **Bibliography ≥ 5 entries** | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 |
| **Overfull `\hbox`** | ✅ 0 | ✅ 0 | ✅ 0 | ✅ 0 |
| **Underfull `\hbox`** | ✅ 2 | ✅ 0 | ✅ 1 | ✅ 1 |
| **LaTeX fatal errors** | ✅ None | ✅ None | ✅ None | ✅ None |
| **Duplicate `\input` chapters** | ✅ None | ✅ None | ✅ None | ✅ None |
| **TikZ anchor warnings** | ✅ None | ✅ None | ✅ None | ✅ None |
| **Orphan bib entries** | ⚠️ 1 | ⚠️ 3 | ✅ None | ⚠️ 1 |
| **Hyperref token warnings** | ℹ️ 36 | ℹ️ 42 | ℹ️ 43 | ℹ️ 43 |

---

## Detailed Findings by Article

### 1 · `1_sine_wave/main.pdf`

**Status: 1 failure, 1 informational**

| # | Severity | Finding |
|---|----------|---------|
| 1 | ❌ FAIL | **Running header absent on 12/15 pages.** `\fancyhead[L]{\leftmark}` is configured correctly, but with 9 single-page chapters the `plain` pagestyle (chapter-opening) dominates. The running head appears on pg 3 (TOC cont.), pg 7, pg 10 only — i.e. pages where a chapter spills to a second side. |
| 2 | ⚠️ INFO | **Orphan bib entry:** `devlin2019bert` is declared in `refs.bib` but never cited in any chapter. |
| 3 | ✅ OK | All other rubric criteria pass: pages=15, footer on 14/15, BiDi clean, 2 tables, 6 math blocks, 2 matplotlib PNGs, 9 unique citations all resolved. |

---

### 2 · `2_security/main.pdf`

**Status: 3 failures, 3 informational**

| # | Severity | Finding |
|---|----------|---------|
| 1 | ❌ FAIL | **Running header absent on 13/15 pages.** Same structural cause as Article 1 (10 short chapters). Running head detected only on pg 3 (TOC) and pg 7. |
| 2 | ❌ FAIL | **Broken citation:** `\cite{devlin2019bert}` appears in `chapters/ch9.tex` (line 6) but `devlin2019bert` is **not** in `refs.bib`. LaTeX log confirms: `"Citation 'devlin2019bert' on page 12 undefined"`. The rendered PDF shows `[?]` at that position. |
| 3 | ❌ FAIL | **biblatex entry-not-found:** Log line `"Warning: The following entry could not be found"` corroborates the missing ref above. |
| 4 | ⚠️ INFO | **3 orphan bib entries:** `brown2020language`, `park2024hybrid`, `vaswani2017attention` are in `refs.bib` but never cited. These are likely copy-paste artifacts from another article's bibliography. |
| 5 | ✅ OK | Pages=15, footer 14/15, BiDi clean, 2 tables, 3 display-math envs, 2 PNGs, no Overfull/Underfull hboxes. |

---

### 3 · `3_xlstm/main.pdf`

**Status: 1 failure, 0 informational — best citation hygiene**

| # | Severity | Finding |
|---|----------|---------|
| 1 | ❌ FAIL | **Running header absent on 13/15 pages.** 10 chapters across 11 content pages; running head visible on pg 3 and pg 9 only. |
| 2 | ✅ OK | **Perfect citation alignment:** all 10 `refs.bib` keys are cited, all 10 `\cite{}` calls resolve. Zero orphan entries. |
| 3 | ✅ OK | Pages=15, footer 14/15, BiDi clean, 3 tables, 6 display-math envs, 2 PNGs, 1 Underfull hbox (badness < 2200), no fatal errors. |

---

### 4 · `4_orchestration/main.pdf`

**Status: 1 failure, 1 informational**

| # | Severity | Finding |
|---|----------|---------|
| 1 | ❌ FAIL | **Running header absent on 13/15 pages.** Same structural cause. Running head on pg 3 and pg 9 only. |
| 2 | ⚠️ INFO | **Orphan bib entry:** `devlin2019bert` is in `refs.bib` but never cited (identical pattern to Article 1). |
| 3 | ✅ OK | Pages=15, footer 14/15, BiDi clean, 3 tables, 5 display-math envs, 2 PNGs, 1 Underfull hbox, no fatal errors, all 9 citations resolved. |

---

## Cross-Cutting Issues

### Issue A — Structural: Running Headers Almost Absent (All 4 Articles)

The `fancyhdr` setup is architecturally correct (uses `\AfterEndPreamble`, defines `\fancypagestyle{plain}` override). However, with 9–10 chapters spread across 11 content pages, **every chapter occupies ≈ 1 page**. In LaTeX's `report` class, the first page of each `\chapter{}` always uses the `plain` pagestyle — which has no header by design. Because nearly every page is a chapter-opening page, the `\fancyhead[L]{\leftmark}` running head is rendered on only 2–3 of 15 pages.

> **Root cause:** Chapter density too high for headers to be visible. The fancyhdr code is correct; the document structure defeats it.

### Issue B — Citation Integrity: `devlin2019bert` Pattern

- **Article 1:** Has `devlin2019bert` in refs.bib but **never cites it**.
- **Article 2:** **Cites** `devlin2019bert` (ch9, line 6) but it's **absent from refs.bib** → broken citation `[?]`.
- **Article 4:** Has `devlin2019bert` in refs.bib but **never cites it**.

This suggests a copy-paste error: the entry was added to refs.bib in articles 1 and 4 without a corresponding citation, and in article 2 a citation was added without adding the bib entry.

### Issue C — Display Math Density

Article 2 has only 3 display-math environments vs 5–6 in the other three. While this passes the rubric minimum of ≥ 1, it is notably lower and may reflect thinner technical exposition in the security article's chapters.

### Issue D — Hyperref Token Warnings (Non-blocking)

All 4 PDFs produce 36–43 `Package hyperref Warning: Token not allowed in a PDF string` warnings. These arise from Hebrew text in section headings appearing in PDF bookmarks/metadata. This is a known limitation of using Hebrew (`polyglossia`) with `hyperref` and does not affect rendering — it is informational only.

---

## Rubric Pass/Fail Count

| Article | PASS | FAIL | INFO (xfail) |
|---------|:----:|:----:|:------------:|
| 1_sine_wave | 20 | 1 | 1 orphan |
| 2_security | 17 | 3 | 3 orphans |
| 3_xlstm | 21 | 1 | — |
| 4_orchestration | 20 | 1 | 1 orphan |

*(Per article: 22 rubric tests run, xfail tests excluded from PASS/FAIL count)*
