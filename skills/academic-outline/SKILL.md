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
