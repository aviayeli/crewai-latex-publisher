---
name: hebrew-nlp-expert
description: >
  Guides the Writer Agent in producing high-register, grammatically correct
  Hebrew academic prose for a peer-reviewed LuaLaTeX publication.
  Covers non-concatenative morphology, cliticization, academic register,
  and AlephBERT-era Hebrew NLP conventions.
metadata:
  author: Avi Ayeli
  version: "1.0"
  skill_spec: "S = <C, π, T, R>"
---

# Hebrew NLP Expert — Formal Skill Specification (S = <C, π, T, R>)

---

## C — Applicability Conditions

Activate this skill when **all** of the following hold:

1. The chapter language is Hebrew (`\setmainlanguage{hebrew}` is active in preamble).
2. The content agent is producing prose that will be compiled with LuaLaTeX + Polyglossia.
3. The writing register must be academic (peer-reviewed publication level, ≥ B2 CEFR).

**Do NOT apply** when writing English-only code blocks, LTR-only appendices, or
figure captions in English.

---

## π — Execution Policy

### 1. Academic Register (עברית אקדמית)

Write in **high-register Modern Standard Hebrew**:
- Prefer nominal constructions (שם עצם) over verbal where academic tone demands it.
  Example: "הניתוח מראה" → "הניתוח מצביע על" (more nominal/formal).
- Avoid colloquial contractions: never "כי-ש" in formal prose; use "מפני ש" or "בשל".
- Use passive voice for method descriptions: "הוחל אלגוריתם X" (algorithm X was applied).

### 2. Non-Concatenative Morphology

Hebrew uses a root-and-pattern (שורש ומשקל) morphology system:
- Ensure verb conjugations agree with subject in **gender, number, and tense**.
- Foreign terms (Transformer, BERT, xLSTM) take **masculine singular** as default gender.
  Example: "הטרנספורמר הוצג" (not הוצגה).
- Plural: "טרנספורמרים", "מודלים", "שכבות" — use correct mishkal pattern.

### 3. Cliticization (הצמדת מילות יחס)

Hebrew prepositions and conjunctions attach as **proclitics** (prefixes), not separate words:
- Correct: `בטרנספורמר`, `למודל`, `ומנגנון`
- Incorrect: `ב- טרנספורמר` (space after proclitic is a typographical error)
- MILA tokenization rule: no whitespace between proclitic and host word in running text.

### 4. AlephBERT and Hebrew NLP Citations

When referencing Hebrew language models or NLP tools:
- Cite AlephBERT (Seker et al., 2021) for contextual morphological disambiguation.
- Cite dicta-bert (Shmidman et al., 2022) for rabbinic and modern Hebrew.
- Use `\cite{alephbert}` and `\cite{dictabert}` as citation keys in LaTeX.
- Reference the XTREME-R benchmark when comparing multilingual model performance.

### 5. Hebrew Quotation Marks

Use Hebrew typographic marks in running prose:
- `"מונח"` → in LaTeX: `״מונח״` (U+05F4 HEBREW PUNCTUATION GERSHAYIM).
- For foreign terms quoted in Hebrew text: wrap with `\textenglish{"term"}`.

---

## T — Termination Criteria

The skill execution is complete when **all** hold:

1. All Hebrew verbs agree with their subjects in gender and number (manual review).
2. No cliticization whitespace errors: `grep -n 'ב- \|ל- \|כ- '` returns empty.
3. All foreign technical terms (model names, acronyms, variable names) appear inside
   `\textenglish{}` when embedded in Hebrew RTL paragraphs.
4. Academic register: at least one nominal construction per paragraph.
5. Passive voice used for all algorithm/method description sentences.

---

## R — Callable Interface

| Tool / Command | Usage |
|---|---|
| `latex_writer_tool(path, mode="write", content)` | Write first chunk of chapter Markdown |
| `latex_writer_tool(path, mode="append", content)` | Append subsequent sections |
| `\textenglish{term}` | Inline English term inside Hebrew RTL paragraph |
| `\begin{english}…\end{english}` | Multi-line English block (≥ 2 lines) |
| `\cite{key}` | Academic citation (AlephBERT → `\cite{alephbert}`) |
| `markdown_converter_tool(md_path, tex_path)` | Convert Markdown chapter to LaTeX |

**Boundary:** Do NOT call `perplexity_search_tool` from within this skill.
Research is the ResearchAgent's exclusive responsibility.
