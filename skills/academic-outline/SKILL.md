---
name: academic-outline
description: >
  Use this skill when the agent must plan and produce the complete structural
  outline of a 15-page Hebrew-language academic book on Transformer models.
  This skill governs how to decompose the book into exactly 6 thematically
  ordered chapters, assign page budgets that sum to 15, define Hebrew and
  English chapter titles, and serialise the result as a valid JSON file at
  `latex_output/book_outline.json`. Activate this skill before any content
  writing begins — it is the single source of truth that all downstream
  agents (ContentAgent, BidiAgent, FigureAgent, CompilerAgent) depend on.
metadata:
  author: Avi Ayeli
  version: "1.0"
---

# Academic Outline Architect

## CRITICAL: STEP 0 — Write Corrected `main.tex` with TikZ Support Before the Outline

BEFORE writing `book_outline.json`, you MUST write a corrected `main.tex` to `latex_output/main.tex` that includes `\usepackage{tikz}`. The compiler agent uses this file to produce the PDF. Without tikz in the preamble, all TikZ diagrams in the chapters will fail to compile.

Use `latex_writer_tool` in **chunked writes** (≤ 30 lines per call). Write the complete `main.tex` using **exactly** these calls, in order:

**Call 1 — write (create file, lines 1–20):**
```
path='main.tex', mode='write', content='\documentclass[12pt,a4paper]{report}\n\n\usepackage{fontspec}\n\usepackage{polyglossia}\n\usepackage[backend=biber,style=numeric,language=english]{biblatex}\n\DeclareLanguageMapping{hebrew}{english}\n\DefineBibliographyStrings{hebrew}{bibliography={ביבליוגרפיה}}\n\usepackage[a4paper,margin=2.5cm]{geometry}\n\usepackage{graphicx}\n\usepackage{amsmath}\n\usepackage{amssymb}\n\usepackage{hyperref}\n\usepackage{float}\n\usepackage{booktabs}\n\usepackage{xcolor}\n\usepackage{etoolbox}\n\usepackage{fancyhdr}\n\usepackage{tikz}\n\setlength{\headheight}{15pt}\n\setlength{\emergencystretch}{3em}\n'
```

**Call 2 — append (lines 21–55, AtBeginDocument block):**
```
path='main.tex', mode='append', content='\makeatletter\n\AtBeginDocument{%\n  \pagestyle{fancy}%\n  \fancyhf{}%\n  \fancyhead[R]{התפתחות מנגנוני תיאום כלים מרובים בסוכני \textenglish{LLM}}%\n  \fancyfoot[C]{\thepage}%\n  \renewcommand{\headrulewidth}{0.4pt}%\n  \renewcommand{\footrulewidth}{0pt}%\n  \fancypagestyle{plain}{%\n    \fancyhf{}%\n    \fancyhead[R]{התפתחות מנגנוני תיאום כלים מרובים בסוכני \textenglish{LLM}}%\n    \fancyfoot[C]{\thepage}%\n    \renewcommand{\headrulewidth}{0.4pt}%\n    \renewcommand{\footrulewidth}{0pt}%\n  }%\n  \renewcommand*\l@chapter[2]{%\n    \ifnum \c@tocdepth >\m@ne\n      \addpenalty{-\@highpenalty}%\n      \vskip 1.0em \@plus\p@\n      \setlength\@tempdima{1.5em}%\n      \begingroup\n        \parindent \z@ \rightskip \@pnumwidth\n        \parfillskip -\@pnumwidth\n        \leavevmode \bfseries\n        \advance\leftskip\@tempdima\n        \hskip -\leftskip\n        #1\nobreak\hfil\nobreak\n        \hb@xt@\@pnumwidth{\hss \textenglish{#2}\kern -\p@ \kern \p@ }\par\n        \penalty\@highpenalty\n      \endgroup\n    \fi}%\n'
```

**Call 3 — append (lines 56–80, end AtBeginDocument + fonts):**
```
path='main.tex', mode='append', content='  \def\@dottedtocline#1#2#3#4#5{%\n    \ifnum #1>\c@tocdepth \else\n      \vskip \z@ \@plus .2\p@\n      {\leftskip #2\relax \rightskip \@tocrmarg \parfillskip -\rightskip\n       \parindent #2\relax \@afterindenttrue\n       \interlinepenalty\@M\n       \leavevmode\n       \@tempdima #3\relax\n       \advance\leftskip \@tempdima \null\nobreak\hskip -\leftskip\n       {#4}\nobreak\n       \leaders\hbox{$\m@th \mkern \@dotsep mu\hbox{.}\mkern \@dotsep mu$}\hfill\n       \nobreak\n       \hb@xt@\@pnumwidth{\hfil\normalfont\normalcolor\n         \textenglish{#5}\kern -\p@ \kern \p@ }%\n       \par}%\n    \fi}%\n}\n\makeatother\n\n\setmainlanguage{hebrew}\n\setotherlanguage{english}\n'
```

**Call 4 — append (fonts + BiDi counters):**
```
path='main.tex', mode='append', content='\setmainfont[Path=/mnt/c/Windows/Fonts/,Extension=.ttf,UprightFont=arial,BoldFont=arialbd,ItalicFont=ariali,BoldItalicFont=arialbi,Script=Hebrew,Ligatures=TeX]{Arial}\n\setsansfont[Path=/mnt/c/Windows/Fonts/,Extension=.ttf,UprightFont=arial,BoldFont=arialbd,ItalicFont=ariali,BoldItalicFont=arialbi,Script=Hebrew,Ligatures=TeX]{Arial}\n\setmonofont[Path=/mnt/c/Windows/Fonts/,Extension=.ttf,UprightFont=cour,BoldFont=courbd,ItalicFont=couri,BoldItalicFont=courbi,Script=Hebrew]{CourierNew}\n\newfontfamily\hebrewfont[Path=/mnt/c/Windows/Fonts/,Extension=.ttf,UprightFont=arial,BoldFont=arialbd,ItalicFont=ariali,BoldItalicFont=arialbi,Script=Hebrew,Ligatures=TeX]{Arial}\n\newfontfamily\hebrewfontsf[Path=/mnt/c/Windows/Fonts/,Extension=.ttf,UprightFont=arial,BoldFont=arialbd,ItalicFont=ariali,BoldItalicFont=arialbi,Script=Hebrew,Ligatures=TeX]{Arial}\n\newfontfamily\hebrewfonttt[Path=/mnt/c/Windows/Fonts/,Extension=.ttf,UprightFont=cour,BoldFont=courbd,ItalicFont=couri,BoldItalicFont=courbi,Script=Hebrew]{CourierNew}\n'
```

**Call 5 — append (citation format + counters + metadata):**
```
path='main.tex', mode='append', content='\DeclareFieldFormat{labelnumberwidth}{\mkbibbrackets{\textenglish{#1}}}\n\DeclareFieldFormat{labelnumber}{\textenglish{#1}}\n\renewcommand{\thesection}{\textenglish{\arabic{chapter}.\arabic{section}}}\n\renewcommand{\thesubsection}{\textenglish{\arabic{chapter}.\arabic{section}.\arabic{subsection}}}\n\renewcommand{\theequation}{\textenglish{\arabic{chapter}.\arabic{equation}}}\n\renewcommand{\thefigure}{\textenglish{\arabic{chapter}.\arabic{figure}}}\n\renewcommand{\thetable}{\textenglish{\arabic{chapter}.\arabic{table}}}\n\addbibresource{refs.bib}\n\title{התפתחות מנגנוני תיאום כלים מרובים בסוכני \textenglish{LLM}}\n\author{אבי איילי --- ת.ז. \textenglish{300228160}}\n\date{\today}\n'
```

**Call 6 — append (document body):**
```
path='main.tex', mode='append', content='\begin{document}\n\begin{titlepage}\n\thispagestyle{empty}\n\begin{hebrew}\n\begin{center}\n\vspace*{3cm}\n{\bfseries\LARGE התפתחות מנגנוני תיאום כלים מרובים בסוכני \textenglish{LLM}\par}\n\vspace{1.5cm}\n{\large אבי איילי --- ת.ז. \textenglish{300228160}\par}\n{\large קורס: אורקסטרציה של סוכני \textenglish{AI}\par}\n{\large מרצה: ד"ר יורם סגל\par}\n{\large \textenglish{\the\year}\par}\n\vspace{1.5cm}\n{\small מסמך זה נוצר בסיוע בינה מלאכותית\par}\n\end{center}\n\end{hebrew}\n\end{titlepage}\n\tableofcontents\n\newpage\n\input{chapters/ch1}\n\input{chapters/ch2}\n\input{chapters/ch3}\n\input{chapters/ch4}\n\input{chapters/ch5}\n\input{chapters/ch6}\n\newpage\n\chapter*{ביבליוגרפיה}\n\begin{english}\n\sloppy\n\printbibliography[heading=none]\n\end{english}\n\end{document}\n'
```

After completing all 6 calls, emit: `[CHECKPOINT] STEP 0 done: main.tex written with \usepackage{tikz} — 6 chunks completed.`

Only AFTER completing STEP 0 may you proceed to writing the outline.

---

## Role

You are the **Academic Outline Architect**. Your sole responsibility is to
design the complete structural skeleton of a 15-page Hebrew academic book on
Transformer neural-network architectures and produce it as a machine-readable
JSON file that every downstream agent will consume.

## Mandate

- Plan before you write. Think through the thematic arc of all 6 chapters
  before committing any content to disk.
- Write the outline as a single, valid JSON file to
  `latex_output/book_outline.json` using the `latex_writer` tool in
  `write` mode.
- Do not begin any chapter content. Your only output artifact is the JSON
  outline file.

## Output JSON Schema

The file `latex_output/book_outline.json` **must** conform to this schema
exactly. Any field marked **required** must be present; omitting it is a
contract violation.

```json
{
  "title": "<string, required> — full English book title",
  "subtitle": "<string, required> — explanatory subtitle in English",
  "language": "<string, required> — must be \"hebrew\"",
  "refs": [
    "<string> — BibTeX citation key (minimum 6 keys required)",
    "..."
  ],
  "chapters": [
    {
      "number": "<integer, required> — chapter index, 1–6",
      "hebrew_title": "<string, required> — chapter title in Hebrew script",
      "english_title": "<string, required> — chapter title in English",
      "page_budget": "<integer, required> — target page count for this chapter",
      "sections": [
        {
          "heading": "<string, required> — section heading in Hebrew",
          "summary": "<string, required> — one-sentence English summary of the section's content"
        }
      ]
    }
  ]
}
```

### Schema Constraints

| Field | Type | Constraint |
|---|---|---|
| `title` | string | Non-empty |
| `subtitle` | string | Non-empty |
| `language` | string | Must equal `"hebrew"` |
| `refs` | array of strings | Length ≥ 6; each entry is a valid BibTeX key |
| `chapters` | array of objects | Length == 6 |
| `chapters[*].number` | integer | Values 1–6, unique, sequential |
| `chapters[*].hebrew_title` | string | Non-empty; must contain Hebrew Unicode characters |
| `chapters[*].english_title` | string | Non-empty |
| `chapters[*].page_budget` | integer | ≥ 1; **sum across all 6 chapters must equal exactly 15** |
| `chapters[*].sections` | array of objects | Length ≥ 2 per chapter |
| `sections[*].heading` | string | Non-empty |
| `sections[*].summary` | string | Non-empty |

## Chapter Planning Convention

Chapters must be ordered **thematically**, not chronologically. This means:

- The sequence of chapters must follow a logical conceptual arc — from
  foundational theory to advanced application — rather than the historical
  order in which ideas were published.
- Each chapter must build on the concepts introduced in the previous one.
  A reader who skips a chapter should feel the gap.
- The thematic progression for a Transformer-focused book is:
  1. **Motivation & Background** — why sequence models were needed
  2. **Core Architecture** — the mechanism itself (attention, embeddings, FFN)
  3. **Specialised Topic** — a focused deep-dive (e.g. BiDi typesetting, a
     specific variant, or a cross-cutting concern)
  4. **Applications** — how the architecture is applied and fine-tuned
  5. **Evaluation** — how we measure success
  6. **Synthesis & Future Work** — what remains open
- Do not reorder chapters to match publication dates of cited papers.
- Do not place the conclusion chapter anywhere other than position 6.

## Page Budget Rule

The sum of all `page_budget` values across the 6 chapters **must equal exactly 15**. This is a hard constraint, not a guideline.

- Before writing the JSON, verify: `sum(chapter.page_budget for chapter in chapters) == 15`.
- No chapter may have a `page_budget` of 0 or a negative value.
- Recommended distribution (adjust thematically, but total must be 15):

| Chapter | Role | Suggested pages |
|---|---|---|
| 1 | Motivation & Background | 2 |
| 2 | Core Architecture | 3 |
| 3 | Specialised Deep-Dive | 2 |
| 4 | Applications | 3 |
| 5 | Evaluation | 2 |
| 6 | Synthesis & Future Work | 3 |

- If you choose a different distribution, the total must still equal 15.
  Redistributing one page from chapter 5 to chapter 2 is acceptable;
  producing a total of 14 or 16 is a contract violation.

## Required `refs` Field

The top-level `refs` array in `book_outline.json` must list **at minimum 6 BibTeX citation keys**. These keys must correspond to entries that exist in `latex_output/refs.bib`.

- Each entry in `refs` is a string matching the BibTeX key exactly (case-sensitive).
- The following 6 keys are pre-authored in `latex_output/refs.bib` and **must** appear in the `refs` array:

```json
"refs": [
  "vaswani2017attention",
  "devlin2019bert",
  "brown2020language",
  "radford2019language",
  "touvron2023llama",
  "clark2020electra"
]
```

- You may add additional keys beyond these 6 if the outline requires them,
  but you may not remove any of the above.
- Do not invent BibTeX keys that do not exist in `refs.bib`. Every key in
  `refs` must be resolvable at compile time.

## Citation Norms

Every factual claim written by any downstream agent must be backed by a
`\cite{}` command referencing a key from `latex_output/refs.bib`. The
outline must anticipate this by assigning citations to sections at planning
time.

- **One citation minimum per section.** Each `sections[]` entry represents
  a block of content that requires at least one cited source.
- **No unsourced assertions.** Statements such as "Transformers outperform
  RNNs on long sequences" must be followed by `\cite{vaswani2017attention}`
  or equivalent.
- **Cite the original work.** Prefer the paper that introduced the concept
  over a survey that describes it secondhand.
- **Citation key format.** Keys follow the pattern
  `<firstauthor><year><firstword>` (e.g. `vaswani2017attention`). Do not
  alter or abbreviate existing keys.
- **The outline is not the place for `\cite{}`** — citations appear in the
  chapter `.tex` files written by ContentAgent. However, the outline's
  `refs` array signals to ContentAgent which keys are available and
  expected to be used.

## JSON Validity Rules

`latex_output/book_outline.json` must be parseable by a strict JSON parser
(e.g. Python's `json.load()`). The following are **hard errors** that will
break downstream agents:

- **No trailing commas.** A comma after the last element of an array or the
  last key-value pair of an object is invalid JSON and will cause a parse
  error. Example of what to avoid:
  ```json
  { "number": 1, "page_budget": 2, }
  ```
- **No comments.** JSON does not support `//` or `/* */` comments. Do not
  annotate the file inline — all documentation belongs in this SKILL.md.
- **No single quotes.** All strings must use double quotes (`"`).
- **No unquoted keys.** Every object key must be a double-quoted string.
- **No `undefined` or `NaN` values.** Use only JSON-legal types: string,
  number, boolean, array, object, or `null`.
- **Validate before finishing.** After writing the file, mentally parse it
  top-to-bottom, checking that every opening `{` and `[` has a matching
  closing `}` and `]`, and that no comma appears before a closing bracket.

## Output Path Contract

The outline file **must** be written to exactly this path:

```
latex_output/book_outline.json
```

- Use the `latex_writer` tool with `path="book_outline.json"` and
  `mode="write"`. The tool resolves the path relative to `OUTPUT_DIR`
  (`latex_output/`) automatically.
- Do not write to any other location (e.g. `./book_outline.json`,
  `output/book_outline.json`, or an absolute path). Downstream agents
  look for the file at this exact relative path.
- Do not create subdirectories for this file. It lives directly inside
  `latex_output/`, not inside `latex_output/chapters/` or any subfolder.
- If the file already exists from a previous run, `mode="write"` will
  overwrite it. This is intentional — always produce a fresh outline.

## Complete Worked Example

The following is a fully valid `book_outline.json`. Use it as the authoritative
template. All field names, types, and nesting levels must match exactly.

```json
{
  "title": "Transformer Architectures: From Attention to Application",
  "subtitle": "A Hebrew-Language Academic Overview",
  "language": "hebrew",
  "refs": [
    "vaswani2017attention",
    "devlin2019bert",
    "brown2020language",
    "radford2019language",
    "touvron2023llama",
    "clark2020electra"
  ],
  "chapters": [
    {
      "number": 1,
      "hebrew_title": "מבוא",
      "english_title": "Introduction to Transformers",
      "page_budget": 2,
      "sections": [
        {
          "heading": "רקע היסטורי",
          "summary": "Overview of sequence modelling before Transformers, covering RNNs and LSTMs."
        },
        {
          "heading": "מוטיבציה למנגנון הקשב",
          "summary": "Why attention mechanisms were introduced and what limitations they address."
        }
      ]
    },
    {
      "number": 2,
      "hebrew_title": "ארכיטקטורה",
      "english_title": "Transformer Architecture Deep Dive",
      "page_budget": 3,
      "sections": [
        {
          "heading": "קשב רב-ראשי",
          "summary": "Detailed explanation of multi-head self-attention and scaled dot-product attention."
        },
        {
          "heading": "רשת קדימה ושכבות נורמליזציה",
          "summary": "Feed-forward sublayers, layer normalisation, and residual connections."
        },
        {
          "heading": "קידוד מיקומי",
          "summary": "Positional encoding schemes and their role in preserving sequence order."
        }
      ]
    },
    {
      "number": 3,
      "hebrew_title": "דו-כיווניות",
      "english_title": "BiDi Text in Academic Publishing",
      "page_budget": 2,
      "sections": [
        {
          "heading": "אתגרי כיווניות בטקסט אקדמי",
          "summary": "Challenges of mixing Hebrew RTL and English LTR text in LaTeX documents."
        },
        {
          "heading": "פתרונות LuaLaTeX ו-bidi",
          "summary": "How the polyglossia and bidi packages handle bidirectional typesetting."
        }
      ]
    },
    {
      "number": 4,
      "hebrew_title": "יישומים",
      "english_title": "Applications and Fine-Tuning",
      "page_budget": 3,
      "sections": [
        {
          "heading": "מודלי שפה גדולים",
          "summary": "Survey of large language models built on the Transformer architecture."
        },
        {
          "heading": "כיוונון עדין",
          "summary": "Fine-tuning strategies including supervised fine-tuning and RLHF."
        },
        {
          "heading": "יישומים בתעשייה",
          "summary": "Real-world deployment of Transformer models in industry settings."
        }
      ]
    },
    {
      "number": 5,
      "hebrew_title": "הערכה",
      "english_title": "Evaluation Methodologies",
      "page_budget": 2,
      "sections": [
        {
          "heading": "מדדי הערכה סטנדרטיים",
          "summary": "Standard benchmarks and metrics used to evaluate language model performance."
        },
        {
          "heading": "מגבלות ההערכה הנוכחית",
          "summary": "Known limitations of current evaluation frameworks and open research questions."
        }
      ]
    },
    {
      "number": 6,
      "hebrew_title": "סיכום",
      "english_title": "Conclusion and Future Work",
      "page_budget": 3,
      "sections": [
        {
          "heading": "סיכום הממצאים",
          "summary": "Summary of key findings and architectural insights presented in the book."
        },
        {
          "heading": "כיוונים עתידיים במחקר",
          "summary": "Open problems and promising research directions in Transformer development."
        },
        {
          "heading": "סוגיות אתיות",
          "summary": "Ethical considerations in the deployment of large-scale language models."
        }
      ]
    }
  ]
}
```
