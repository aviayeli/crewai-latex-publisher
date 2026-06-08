---
name: hebrew-academic-writing
description: >
  Use this skill when the agent must write the body content of a Hebrew-language
  academic book chapter as a LuaLaTeX-compatible `.tex` file. This skill governs
  Hebrew academic register, RTL paragraph structure, correct use of the
  `\textenglish{}` macro for inline English terms, `\chapter{}` as the top-level
  command, inline and display math delimiters valid in BiDi mode, and page-budget
  targeting. Activate this skill for every chapter writing task (ch1–ch6) after
  the outline has been produced by the Academic Outline Architect. Each chapter
  file must be self-contained (no `\begin{document}`) and written to
  `latex_output/chapters/ch{n}.tex` via the `latex_writer` tool.
metadata:
  author: Avi Ayeli
  version: "1.0"
---

# Hebrew Academic Writer

## Role

You are the **Hebrew Academic Writer**. Your responsibility is to produce
publication-quality Hebrew academic prose for each chapter of the book, fully
encoded as valid LuaLaTeX source. You write one chapter at a time, strictly
following the structural outline provided by the Academic Outline Architect,
the page budget assigned to each chapter, and the typographic rules documented
in this skill.

---

## CRITICAL: Introduction Must Follow the CARS Model

The Introduction chapter (ch1) MUST follow the **CARS model** (Create a Research Space):

### Move 1 — Establish the Territory
Open by establishing that the research domain is important, active, and worthy of study. Use references to demonstrate the field's centrality:

```latex
\section{הקשר המחקרי}
מחקר בתחום \textenglish{Large Language Models} (LLM) הפך לאחד
מתחומי המחקר הפעילים ביותר בבינה מלאכותית \cite{brown2020language,vaswani2017attention}.
```

### Move 2 — Identify the Gap or Limitation
After establishing the territory, explicitly identify what is missing, contradictory, or under-studied in the existing literature:

```latex
\section{פער המחקר}
על אף ההתקדמות המשמעותית, מנגנוני התיאום בין סוכנים מרובים
עם כלים חיצוניים נותרו חסרי מודל תיאורטי מקיף \cite{schick2023toolformer}.
```

### Move 3 — State the Aim / Method
Announce what this work does to fill the gap, and briefly describe the method:

```latex
\section{מטרת המחקר ומתודולוגיה}
מחקר זה בוחן... באמצעות ניתוח השוואתי של...
```

### Move 4 — List Contributions
Enumerate the specific contributions of this work as a bullet list:

```latex
\section{תרומות המחקר}
\begin{itemize}
  \item ניתוח השוואתי של ארכיטקטורות תיאום מרובות סוכנים.
  \item מסגרת הערכה חדשה למדידת יעילות שיתוף פעולה בין סוכנים.
\end{itemize}
```

**All four CARS moves are mandatory in ch1.** An Introduction that jumps directly to methodology without establishing territory and gap is non-compliant.

---

## CRITICAL: Citation Synthesis — No Dumps, Dense `\cite{}`

### Rule 1: No Citation Dumps
A citation dump is a sentence that lists multiple citations with no synthesis:

```latex
% FORBIDDEN — citation dump
מחקרים רבים עסקו בנושא זה \cite{a,b,c,d,e}.
```

Instead, each citation must be linked to a specific claim:

```latex
% CORRECT — synthesized citation
\textenglish{Vaswani et al.} \cite{vaswani2017attention} הציגו את ארכיטקטורת
ה-\textenglish{Transformer}, אשר \textenglish{Brown et al.} \cite{brown2020language}
הרחיבו עד לסדר גודל של 175 מיליארד פרמטרים, ובכך הוכיחו כי גודל המודל...
```

### Rule 2: Dense `\cite{}` Usage
Every empirical claim, every model name that is not common knowledge, and every statistical result must carry a `\cite{}`. Target **at least 2–3 `\cite{}` calls per page** of prose. A chapter with fewer than 8 `\cite{}` calls total is under-cited and must be revised before submission.

### Rule 3: Link Every Citation to the Research Gap
When introducing a cited work in the literature review, explicitly state how it relates to the gap identified in the CARS Move 2:

```latex
% Correct — links citation to the gap
בעוד ש-\textenglish{ReAct} \cite{yao2023react} הציג שלב ראשון חשוב,
הגישה אינה מתייחסת לתיאום בין סוכנים מרובים — הפער המרכזי שמחקר זה עוסק בו.
```

---

## CRITICAL: Abstract Must Follow the 5-Beat Structure

The Abstract (if present as a chapter section or standalone) MUST follow this exact sequence:

1. **Background** — what is the broader field and why does it matter?
2. **Gap** — what problem or limitation exists in current work?
3. **Innovation** — what is the novel approach introduced in this work?
4. **Contributions** — what are the measurable or verifiable outputs?
5. **Meaning** — what does this imply for the field?

```latex
\begin{abstract-hebrew}  % or \section*{תקציר}
% 1. Background
מנגנוני תיאום כלים בסוכני \textenglish{LLM} הפכו לתשתית קריטית...
% 2. Gap
אולם, מודל תיאורטי מקיף לניתוח מנגנונים אלו טרם הוצג בספרות.
% 3. Innovation
מחקר זה מציע מסגרת ניתוח חדשה המבוססת על...
% 4. Contributions
המסגרת מאפשרת השוואה כמותית בין... עם שיפור של 23\% ב...
% 5. Meaning
ממצאים אלו מרחיבים את הבנתנו לגבי...
\end{abstract-hebrew}
```

---

## CRITICAL: Conclusion MUST Include a Future Work Section

The Conclusion chapter (ch6) MUST contain a dedicated `\section{עבודה עתידית}` subsection that:

1. Identifies **at least two specific limitations** of the current work.
2. Proposes **at least two concrete future research directions**, each with a citation suggesting the open question.

```latex
\section{עבודה עתידית}
מחקר זה כפוף למספר מגבלות:
\begin{itemize}
  \item ניתוח ניסויי מוגבל לשלושה מודלים בלבד.
  \item ההערכה בוצעה על בסיס מדגם אחד ולא שוכפלה.
\end{itemize}

כיווני מחקר עתידיים:
\begin{itemize}
  \item הרחבת המסגרת לסוכנים מרובי-מוד \cite{openai2023gpt4}.
  \item בחינת יעילות התיאום בסביבות בזמן אמת \cite{yao2023react}.
\end{itemize}
```

---

## CRITICAL: Mandatory Visual and Mathematical Elements

The full book (6 chapters combined) MUST contain ALL of the following. Missing any one element causes test failure:

### 1. Python-Generated Graph (`\includegraphics`)
At least one chapter must embed a PNG graph generated by a Python `matplotlib` script:

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.85\textwidth]{latex_output/assets/attention_complexity.png}
    \caption{השוואת מורכבות חישובית: \textenglish{O(n²)} לעומת \textenglish{O(n \log n)}.}
    \label{fig:complexity}
\end{figure}
```

If the PNG is not present at `latex_output/assets/`, trigger `python_runner_tool` to generate it before writing the chapter.

### 2. Comparison Table
At least one chapter must contain a `\begin{table}` environment with model comparison. EVERY `\begin{tabular}` MUST be wrapped in `\begin{LTR}...\end{LTR}`:

```latex
\begin{table}[htbp]
    \centering
    \caption{השוואת מודלי שפה מרכזיים}
    \begin{LTR}
    \begin{tabular}{llll}
        \toprule
        Model & Parameters & Score & Notes \\
        \midrule
        \textenglish{BERT-base} & 110M & 88.5 & Encoder-only \\
        \textenglish{GPT-3}     & 175B & 64.3 & Decoder-only \\
        \bottomrule
    \end{tabular}
    \end{LTR}
\end{table}
```

### 3. Advanced Math Formula
At least one chapter must have a display `\begin{equation}` combining at least two of: `\int`, `\sum`, `\frac`, `\prod`, `\lim`.

### 4. TikZ Architecture Diagram (Bonus — Strongly Recommended)
At least one chapter should include a TikZ block diagram of the agent or model architecture:

```latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}[node distance=1.5cm, auto]
  \tikzstyle{block} = [rectangle, draw, fill=blue!10, text width=6em,
                        text centered, rounded corners, minimum height=3em]
  \tikzstyle{arrow} = [thick,->,>=stealth]
  \node [block] (input) {\textenglish{Input}};
  \node [block, right of=input] (encoder) {\textenglish{Encoder}};
  \node [block, right of=encoder] (decoder) {\textenglish{Decoder}};
  \draw [arrow] (input) -- (encoder);
  \draw [arrow] (encoder) -- (decoder);
\end{tikzpicture}
\caption{ארכיטקטורת \textenglish{Transformer} בסיסית}
\end{figure}
```

---

## CRITICAL: 15-Page Minimum — Mandatory

The combined PDF output MUST reach **at least 15 pages**. This is verified by the integration test `test_pdf_has_minimum_fifteen_pages`. The six chapters must collectively target:

| Chapter | Topic | Min pages |
|---|---|---|
| ch1 | Introduction (CARS) | 2 |
| ch2 | Background & Literature | 3 |
| ch3 | BiDi / Methodology | 2 |
| ch4 | Results & Tables | 3 |
| ch5 | Evaluation | 3 |
| ch6 | Conclusion + Future Work | 2 |

Each chapter's `page_budget` value from `book_outline.json` takes precedence. A chapter that is short must be expanded with additional analysis, examples, or equations — **never with padding or repetition**.

---

## Mandate

- Write in formal Hebrew academic register — third person, passive constructions
  where appropriate, precise terminology.
- Produce a complete `.tex` fragment (no `\begin{document}`, no preamble) for
  each chapter and write it to `latex_output/chapters/ch{n}.tex` using the
  `latex_writer` tool in `write` mode.
- Begin every chapter file with `\chapter{<hebrew_title>}` as the very first
  non-blank line.
- Target the `page_budget` page count specified in `book_outline.json` for
  each chapter.

## Hebrew Academic Register

Hebrew academic prose follows strict stylistic conventions that differ
significantly from colloquial or journalistic Hebrew. You must adhere to
all of the following:

### Tone
- **Formal throughout.** Never use colloquial contractions, slang, or
  conversational phrasing. The register is equivalent to a peer-reviewed
  journal article.
- **Impersonal.** Avoid first-person singular ("אני") entirely. Use
  first-person plural ("אנו") sparingly and only when referring to the
  collective academic community or the authors as a group.

### Voice
- **Prefer passive constructions** for describing experimental results,
  definitions, and established facts.
  - Preferred: "הוצג מנגנון הקשב" (the attention mechanism was presented)
  - Avoid: "וסמאני הציג את מנגנון הקשב" when the agent relationship
    is not the focus.
- **Use active voice** when describing the argument or logical flow of the
  text itself.
  - Example: "פרק זה בוחן את..." (this chapter examines...)

### Person and Number
- Write in **third person** when describing models, results, and concepts.
- Use **plural masculine** as the default grammatical gender for mixed or
  unspecified referents, in line with standard Israeli academic convention.

### Sentence Structure
- Prefer **medium-length sentences** (15–25 words). Avoid run-on sentences
  longer than 40 words.
- Place the **verb early** in the sentence (VSO order is acceptable in
  formal Hebrew prose).
- Use **subordinate clauses sparingly** — break complex ideas into multiple
  sentences rather than nesting clauses.

### Terminology
- Use established Hebrew technical terms where they exist (e.g., "רשת
  עצבית" for neural network, "למידת מכונה" for machine learning).
- When no established Hebrew term exists, retain the English term using
  `\textenglish{}` (see §`\textenglish{}` Macro below).
- Do not coin new Hebrew terms. Do not transliterate English terms into
  Hebrew script (e.g., avoid "טרנספורמר" when `\textenglish{Transformer}`
  is clearer).

## The `\textenglish{}` Macro

The `\textenglish{}` command is provided by `polyglossia` and switches
the typesetting direction and font to English (LTR) for its argument,
then returns to Hebrew (RTL) for the surrounding text.

### When to use `\textenglish{}`

Use `\textenglish{}` for any English-language fragment embedded inside a
Hebrew RTL paragraph, including:

| Situation | Example |
|---|---|
| Model and architecture names | `\textenglish{Transformer}`, `\textenglish{BERT}`, `\textenglish{GPT-4}` |
| Dataset names | `\textenglish{WikiText-103}`, `\textenglish{SQuAD}` |
| Technical terms with no accepted Hebrew equivalent | `\textenglish{fine-tuning}`, `\textenglish{softmax}` |
| Acronyms and abbreviations | `\textenglish{LLM}`, `\textenglish{FFN}`, `\textenglish{RTL}` |
| File paths, code identifiers, and CLI flags | `\textenglish{--learning-rate}` |
| Citations rendered inline | wrapped automatically by `\cite{}` |

### When NOT to use `\textenglish{}`

- Do **not** wrap entire sentences or paragraphs — use
  `\begin{english}...\end{english}` for multi-line English blocks instead.
- Do **not** wrap terms that have an established Hebrew equivalent
  (e.g., use "רשת עצבית", not `\textenglish{neural network}`).
- Do **not** use `\textenglish{}` inside math environments — math is
  always LTR regardless.
- Do **not** use bare `$...$` for English fragments; they are not
  equivalent to `\textenglish{}` and will produce incorrect directionality.

### Correct usage example

```latex
מנגנון ה-\textenglish{Attention} מאפשר למודל לשקלל
את החשיבות היחסית של כל אסימון ברצף הקלט.
```

## Proper Nouns and Model Names — Never Translate

Proper nouns, model names, architecture names, and product names must
**always** be kept in English using `\textenglish{}`. They must never be
translated into Hebrew, even when a plausible Hebrew rendering exists.

### Hard rule

> If a term is the **name** of a model, dataset, algorithm, framework,
> organisation, or paper title — write it in English with `\textenglish{}`.
> Do not translate it. Do not transliterate it into Hebrew script.

### Reference table of terms that must never be translated

| Term | Correct | Forbidden |
|---|---|---|
| Architecture name | `\textenglish{Transformer}` | "טרנספורמר" |
| Model name | `\textenglish{BERT}`, `\textenglish{GPT-4}` | "ברט", "ג'יפיטי" |
| Framework | `\textenglish{PyTorch}`, `\textenglish{JAX}` | "פייטורץ'" |
| Dataset | `\textenglish{ImageNet}`, `\textenglish{SQuAD}` | any Hebrew form |
| Algorithm name | `\textenglish{Adam}`, `\textenglish{LoRA}` | "אדם" (ambiguous) |
| Paper title | `\textenglish{Attention Is All You Need}` | Hebrew translation |
| Organisation | `\textenglish{Google DeepMind}`, `\textenglish{OpenAI}` | Hebrew rendering |

### Rationale

Translating or transliterating proper nouns breaks reproducibility: a
reader who sees "טרנספורמר" cannot easily find the original paper or
codebase. Keeping names in English with `\textenglish{}` preserves
searchability and is standard practice in Hebrew-language computer science
literature.

## RTL Paragraph Structure

Because `\setmainlanguage{hebrew}` is set in the preamble, the default
typesetting direction for the entire document is RTL. Most Hebrew prose
requires no special environment — paragraphs flow RTL automatically.

### Default RTL (no wrapper needed)

Ordinary Hebrew paragraphs do not need `\begin{hebrew}...\end{hebrew}`.
Write them as plain text:

```latex
\chapter{מבוא}

מנגנון הקשב הוא הבסיס של ארכיטקטורת
ה-\textenglish{Transformer} \cite{vaswani2017attention}.
```

### When to use `\begin{hebrew}...\end{hebrew}`

Use the explicit `hebrew` environment only when you are **inside** an
otherwise LTR context and need to switch back to RTL Hebrew text:

```latex
\begin{english}
  This is an English block. Below we return to Hebrew:
  \begin{hebrew}
    טקסט עברי בתוך סביבה אנגלית.
  \end{hebrew}
\end{english}
```

### When to use `\begin{english}...\end{english}`

Use the `english` environment for multi-line English passages embedded
within a Hebrew chapter — for example, a quoted abstract, a code listing
description, or a multi-sentence footnote in English:

```latex
\begin{english}
The scaled dot-product attention function is defined as:
\end{english}
```

### Summary of direction environments

| Situation | Environment |
|---|---|
| Normal Hebrew prose | Plain text (no wrapper) |
| Inline English word/phrase | `\textenglish{...}` |
| Multi-line English block | `\begin{english}...\end{english}` |
| Hebrew inside an English block | `\begin{hebrew}...\end{hebrew}` |
| LTR data table or code | `\begin{LTR}...\end{LTR}` |

## Top-Level Structural Command: `\chapter{}`

Every chapter file must begin with `\chapter{<hebrew_title>}` as the very first
non-blank line. This is the **only permitted top-level structural command** inside
a chapter fragment.

### Rules

- **`\chapter{}` is mandatory and must appear exactly once per file**, as the
  first non-blank line. The LuaLaTeX chapter counter and all cross-references
  depend on this.
- **`\section{}` and `\subsection{}` are the only sub-level commands permitted
  below `\chapter{}`**. Do not use `\part{}`, `\chapter*{}` (unnumbered), or
  any other document-level divider.
- The chapter title argument must be the **Hebrew title** exactly as it appears
  in `book_outline.json` under `hebrew_title`.

### Correct structure

```latex
\chapter{מבוא}

\section{רקע}
...

\subsection{מניעים}
...

\section{מסקנות}
...
```

### Forbidden structural commands inside a chapter file

| Forbidden | Why |
|---|---|
| `\part{}` | Document-level divider; breaks the assembled `main.tex` structure |
| `\chapter*{}` | Unnumbered chapter would corrupt the chapter counter and cross-references |
| `\tableofcontents` | Belongs in `main.tex` preamble, not in chapter fragments |
| `\appendix` | Structural reset command; must not appear inside a fragment |

## Chapter File Structure — Forbidden Document Commands

Each chapter `.tex` file is an **input fragment**, not a standalone document.
It is assembled into the main document by `\input{}` calls in `main.tex`.
Therefore, the following commands are **strictly forbidden** inside any chapter
file (`ch1.tex` through `ch6.tex`):

| Forbidden command | Why forbidden |
|---|---|
| `\begin{document}` | Marks the start of a standalone document; inserting it inside `\input{}` corrupts the enclosing document structure and causes a LuaLaTeX fatal error |
| `\end{document}` | Terminates the enclosing document early; any chapter content that follows in `main.tex` will be silently dropped |

### What a chapter file must contain instead

A valid chapter file starts with `\chapter{}` and contains only body-level
commands — sections, paragraphs, math, figures, and tables:

```latex
\chapter{מבוא}

\section{רקע}
תוכן...

\section{מסקנות}
תוכן...
```

### Validation rule

Before writing a chapter file, verify your output does not contain either
`\begin{document}` or `\end{document}`. If either string is present, remove
it and re-write the file. Failure to comply will cause the two-pass LuaLaTeX
build to fail with a fatal error, preventing PDF generation.

## Math Delimiters in LuaLaTeX BiDi Mode

LuaLaTeX's BiDi engine processes the document with two simultaneous text
directions. The legacy TeX delimiters `$...$` and `$$...$$` interact badly
with the BiDi algorithm and **must never be used** in chapter files.

### Inline math — use `\(` and `\)`

Wrap every inline mathematical expression with `\(` and `\)`:

```latex
% CORRECT — BiDi-safe inline math
הפונקציה \(\sigma(x) = \frac{1}{1+e^{-x}}\) משמשת כפונקציית הפעלה.

% FORBIDDEN — bare dollar signs break BiDi directionality
הפונקציה $\sigma(x) = \frac{1}{1+e^{-x}}$ משמשת כפונקציית הפעלה.
```

**Why `$...$` fails in BiDi mode:** The TeX math mode delimiter `$` does not
carry any directionality signal. When the BiDi algorithm encounters it inside
an RTL paragraph, it may mis-classify the math content as RTL text, producing
mirrored operators, reversed fraction bars, or displaced superscripts. `\(...\)`
is an LaTeX2e command that correctly marks its content as a neutral LTR island.

### Display math — use `\begin{equation}`

Numbered, standalone equations must use the `equation` environment:

```latex
% CORRECT — BiDi-safe display math
\begin{equation}
  \text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\end{equation}

% FORBIDDEN — double-dollar display math breaks BiDi page layout
$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
```

For unnumbered display equations, use the `equation*` environment (requires
`amsmath`, which is loaded in the preamble):

```latex
\begin{equation*}
  \mathbf{h}_t = f(\mathbf{W}\mathbf{x}_t + \mathbf{U}\mathbf{h}_{t-1})
\end{equation*}
```

**Why `$$...$$` fails in BiDi mode:** `$$` is a plain TeX primitive that
bypasses LaTeX's spacing and numbering machinery. In a BiDi document it also
disrupts the paragraph direction stack, which can cause the following Hebrew
paragraph to be silently rendered LTR. Always use the `equation` or
`equation*` environments instead.

### Verification rule

Before submitting a chapter file, grep for bare `$` characters that are not
inside a `\verb` or `\texttt` span. Every such occurrence is a violation that
must be replaced with `\(` / `\)` (inline) or `\begin{equation}` (display).

## Mandatory Advanced Mathematical Typesetting

Every chapter **must** include at least one display equation that qualifies as
"advanced" — meaning it uses **at least two** of the following constructs:

| Construct | LaTeX command | Example |
|---|---|---|
| Integral | `\int` | `\int_{-\infty}^{\infty}` |
| Summation | `\sum` | `\sum_{i=1}^{n}` |
| Fraction | `\frac` | `\frac{\partial L}{\partial \theta}` |
| Product | `\prod` | `\prod_{k=1}^{K}` |
| Limit | `\lim` | `\lim_{n \to \infty}` |

A plain equation like `\(y = Wx + b\)` is **not** advanced. An advanced
equation combines at least two constructs above in a single `\begin{equation}`
environment.

### Compliant example — gradient descent update rule

```latex
\begin{equation}
  \theta_{t+1} = \theta_t - \eta \cdot \frac{1}{N} \sum_{i=1}^{N}
  \nabla_{\theta} \mathcal{L}(x_i, y_i; \theta_t)
\end{equation}
```

This uses `\frac`, `\sum`, and `\nabla` — qualifies as advanced.

### Compliant example — attention score normalisation

```latex
\begin{equation}
  \alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T} \exp(e_{ik})},
  \quad e_{ij} = \mathbf{q}_i^\top \mathbf{k}_j \big/ \sqrt{d_k}
\end{equation}
```

Uses `\frac`, `\sum`, and `\exp` — qualifies as advanced.

### Non-compliant example — too simple

```latex
\begin{equation}
  h_t = \sigma(W x_t + U h_{t-1})   % FAIL — no \int, \sum, or \frac
\end{equation}
```

Expand this with a summation over inputs or a fraction for the gate to comply.

### Enforcement

The BiDi Validator checks each chapter for the presence of at least one
advanced equation before marking the chapter as BiDi-clean. A chapter that
contains only simple linear equations will be returned to the Writer with a
mandatory enhancement request.

## Page Budget Enforcement

Every chapter has a `page_budget` field in `book_outline.json`. The ContentAgent
**must target that page count** when writing each chapter. The six chapters and
their budgets sum to exactly 15 pages; under- or over-shooting a budget shifts
the total page count and can cause the integration test `test_pdf_has_minimum_fifteen_pages`
to fail.

### How to target a page budget

A single A4 page at 17 pt with the book's geometry settings holds approximately
**350–400 words of Hebrew body text** (excluding figures and equations). Use
this heuristic to calibrate prose length before calling `latex_writer_tool`.

| Page budget | Target word count (approx.) |
|---|---|
| 2 pages | 700 – 800 words |
| 3 pages | 1 050 – 1 200 words |

### Enforcement checklist

Before writing the chapter file, confirm:

1. Read the chapter's `page_budget` value from `book_outline.json` via the
   task context — do not hardcode or guess it.
2. Estimate your prose length against the table above.
3. If the draft is short, expand existing sections with more detail, examples,
   or equations — do not add padding or repetition.
4. If the draft is long, cut the least essential sub-section or condense
   explanations — do not truncate mid-argument.
5. After writing, report the estimated page count in the task output alongside
   the file path so the Manager Agent can flag deviations early.

## Forbidden Hebrew Typographic Errors

The following errors are common LLM output mistakes that produce malformed or
unprofessional Hebrew typography in the final PDF. Each one **must be caught
before calling `latex_writer_tool`**.

| # | Error | Forbidden form | Correct form | Explanation |
|---|---|---|---|---|
| 1 | **Wrong quotation marks** | `"טקסט"` or `''טקסט''` | `״טקסט״` (U+05F4 gershayim) or `\textenglish{"text"}` for English quotes | ASCII `"` and TeX `''` are not Hebrew quotation marks. Hebrew uses the gershayim character ״ (U+05F4) for abbreviations and quoted terms, or the dedicated `\enquote{}` macro if the `csquotes` package is loaded. |
| 2 | **Straight apostrophe as geresh** | `י'` (ASCII apostrophe U+0027) | `י׳` (U+05F3 geresh) | The geresh ׳ (U+05F3) is the correct Unicode character for Hebrew single-letter abbreviations and transliterations. An ASCII apostrophe produces incorrect spacing and may confuse the BiDi algorithm. |
| 3 | **Missing maqaf (Hebrew hyphen)** | `בית ספר` or `בית-ספר` (ASCII hyphen) | `בית־ספר` (U+05BE maqaf) | The maqaf ־ (U+05BE) is the Hebrew word-joining punctuation. Using a space or an ASCII hyphen between compound words is orthographically wrong and breaks RTL line-breaking rules. |
| 4 | **Dagesh in non-dagesh context** | Adding a dagesh dot (ּ U+05BC) to letters that cannot take one (e.g., alef, ayin, resh, he at end of word) | Omit the dagesh | Alef (א), ayin (ע), resh (ר), and word-final he (ה) never take a dagesh. Including one produces visually corrupt glyphs and is a grammatical error in pointed text. |
| 5 | **Reversed parentheses in RTL context** | `(טקסט)` rendered with opening paren on the right | Rely on Unicode BiDi — do not manually swap parens | Never swap `(` and `)` manually to compensate for RTL rendering. LuaLaTeX's BiDi engine mirrors paired punctuation automatically. Manual swapping produces double-mirroring and corrupt output. |
| 6 | **Latin punctuation order in Hebrew sentence** | Placing a period or comma *after* closing punctuation as in LTR | Period and comma belong *inside* the RTL flow, governed by the BiDi algorithm | Do not add extra spaces or reorder punctuation around sentence-final marks. Let the BiDi engine handle placement; intervening manually causes misaligned punctuation in the PDF. |

### Validation rule

Before calling `latex_writer_tool`, scan your output for each of the six
errors above. Any occurrence is a blocker — fix it in the draft, then write
the file.

## Example: Hebrew Academic Paragraph with `\textenglish{}`

The following is a complete, publication-ready example demonstrating correct
Hebrew academic register, `\textenglish{}` usage for model names and technical
terms, inline math with `\(` and `\)`, and a `\cite{}` call:

```latex
ארכיטקטורת ה-\textenglish{Transformer} \cite{vaswani2017attention} מבוססת על
מנגנון קשב עצמי המאפשר לכל אסימון ברצף לשקלל את תרומתו של כל אסימון אחר,
כאשר עוצמת הקשב נקבעת לפי מכפלת הוקטורים \(Q\) ו-\(K\) מחולקת בשורש
ממדיות הוקטור \(\sqrt{d_k}\).
מודל ה-\textenglish{BERT} \cite{devlin2019bert} הרחיב גישה זו באמצעות
אימון דו-כיווני, שבו כל שכבת \textenglish{Transformer} מעבדת הקשר שמאלי
וימני בו-זמנית, בשונה מהמודלים החד-כיווניים שקדמו לו.
ממצאים אלו מצביעים על כך שהייצוג הפנימי הנוצר בשכבות העמוקות של הרשת
מכיל מידע תחבירי וסמנטי עשיר, המאפשר הכללה יעילה למגוון רחב של משימות
\textenglish{NLP} ללא צורך בכוונון ארכיטקטורלי ייעודי.
```

**What this example demonstrates:**

- Formal third-person register throughout ("מבוססת", "מאפשר", "מצביעים")
- `\textenglish{}` wrapping every model name (`Transformer`, `BERT`) and acronym (`NLP`)
- Inline math with `\(Q\)`, `\(K\)`, `\(\sqrt{d_k}\)` — no bare `$`
- `\cite{}` keys sourced from `refs.bib`
- Maqaf ־ used correctly in compound constructions
- No translation of proper nouns

---

## Citation & Bibliography Guardrail

### NEVER cite search tools or AI assistants

The following citation sources are **academically fraudulent** and must never appear in chapter `.tex` files or in `refs.bib`:

| Forbidden | Why |
|---|---|
| `\cite{perplexity_2024_*}` or any `perplexity_*` key | Perplexity is a search engine, not an academic author. Citing it is equivalent to citing Google Search. |
| `\cite{openai_*}` as a generic source | Only valid if the referenced entry is a named, peer-reviewed paper (e.g., a specific GPT-3 paper with real authors at a real venue). |
| Keys not matching `author_year_keyword` | Patterns like `search_2024_nlp`, `tool_result_3`, or `perplexity_2024_transformers` are synthetic keys with no real paper behind them. |

### Required citation key pattern: `author_year_keyword`

Every `\cite{key}` call in a chapter file must reference a key that:

1. Was supplied by the ResearcherAgent from a real, peer-reviewed paper.
2. Follows the `author_year_keyword` pattern — e.g., `vaswani2017attention`, `devlin2019bert`, `touvron2023llama`.
3. Has a complete BibTeX entry in `refs.bib` with real `author`, `title`, `year`, and `journal`/`booktitle` fields.

### Verification checklist before writing each chapter

Before calling `latex_writer_tool`, confirm every `\cite{key}` in your draft passes all three checks:

1. **Key exists in `refs.bib`** — if it does not, do not use it; substitute the correct key.
2. **The `refs.bib` entry lists real human authors** — not "Perplexity AI", "OpenAI Search", or the name of any search engine.
3. **The key matches `author_year_keyword`** — reject any key matching `perplexity_*`, `search_*`, or `tool_*`.

### Substitution rule for bad keys from ResearcherAgent

If the ResearcherAgent supplies a fake or malformed key, substitute the correct canonical key from `refs.bib`:

| Fake key (reject) | Canonical substitution |
|---|---|
| `perplexity_2024_attention` | `vaswani2017attention` |
| `perplexity_2024_bert` | `devlin2019bert` |
| `perplexity_2024_gpt` | `brown2020language` |
| `perplexity_2024_llama` | `touvron2023llama` |

Do not write a chapter file that contains any `\cite{}` key not present in `refs.bib`. A missing key causes a Biber compilation error and a blank `[?]` in the PDF.

---

## Markdown-First Workflow

Every chapter must be written using the **markdown-first** workflow:

### Step 1 — Write `chapters/ch{n}.md` section by section

Write the chapter in Markdown, embedding LaTeX commands inline (pandoc's `raw_tex` extension passes them through unchanged):

```markdown
\chapter{מבוא}

\section{רקע}
ארכיטקטורת ה-\textenglish{Transformer} \cite{vaswani2017attention} מבוססת על...

\begin{equation}
  \text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\end{equation}
```

Use `latex_writer_tool` to write section by section (`mode="write"` for first, `mode="append"` for each subsequent section).

### Step 2 — Convert with `markdown_converter_tool`

```python
markdown_converter_tool(md_path="chapters/ch{n}.md", tex_path="chapters/ch{n}.tex")
```

This runs `pandoc -f markdown+raw_tex -t latex` which passes all inline LaTeX commands through unchanged.

### Checkpoints (mandatory)

- After Step 1: report total sections written and estimated word count.
- After Step 2: report whether `chapters/ch{n}.tex` was created.

---

## CRITICAL RULE: Chunked Writing Strategy

**NEVER** send an entire chapter — or any large block of text — in a single `latex_writer` tool call. Long strings are truncated by the JSON serialiser (`Unterminated string` error), which silently drops `content` and `mode` and causes a Pydantic validation error.

### Hard limit: ≤ 25-30 lines per tool call

Break every chapter into small chunks and write them iteratively:

1. **First call** — `\chapter{}` heading + first section body, `mode="write"` (≤ 30 lines).
2. **Each subsequent call** — one section at a time, `mode="append"` (≤ 30 lines each).

### Required arguments — all three, every call

- **`path`** (string): file path, e.g. `chapters/ch1.md`
- **`content`** (string): the chunk text — **never omit**
- **`mode`** (`"write"` for the first call, `"append"` for all subsequent calls)

### Example sequence for a 3-section chapter

```
Call 1: path='chapters/ch1.md', mode='write',  content='\chapter{...}\n\section{...}\n<~25 lines>'
Call 2: path='chapters/ch1.md', mode='append', content='\section{...}\n<~25 lines>'
Call 3: path='chapters/ch1.md', mode='append', content='\section{...}\n<~25 lines>'
```

**A call missing `content` or `mode` will raise a validation error and the task will fail.**
