---
name: perplexity-research
description: Instructs the Academic Researcher agent on how to perform deep internet research using the Perplexity AI sonar-pro API to gather peer-reviewed academic sources specifically about Transformer model architectures, attention mechanisms, and Hebrew NLP. The agent queries Perplexity AI with precise technical terminology, filters results to prioritize primary peer-reviewed sources over secondary blogs or documentation, and produces a structured Markdown research block whose citation keys map directly to BibTeX entries in refs.bib. This skill also documents the OpenAI-compatible API endpoint, Bearer token authentication via PERPLEXITY_API_KEY, rate-limit handling for HTTP 429 responses, and the exact output format required by downstream outline and content agents.
metadata:
  author: Avi Ayeli
  version: "1.0"
---

# Academic Researcher

## Role

The Academic Researcher agent uses the Perplexity AI API to gather peer-reviewed academic sources on Transformer architectures, attention mechanisms, and Hebrew NLP. Its output feeds directly into the Outline Agent: every citation key produced here must appear in `refs.bib` and be citable via `\cite{}` in the chapter `.tex` files.

---

## Perplexity AI API

The Perplexity API is OpenAI-compatible. Use the `/chat/completions` endpoint:

```
POST https://api.perplexity.ai/chat/completions
```

### Authentication

Pass the API key as a Bearer token in the `Authorization` header:

```
Authorization: Bearer <PERPLEXITY_API_KEY>
```

The key is loaded from `settings.PERPLEXITY_API_KEY`. Never hardcode the key in Python source.

### Model

Always use:

```json
"model": "sonar-pro"
```

`sonar-pro` is the Perplexity model optimised for academic and technical search with inline citations. Do not substitute another model — other models do not return source URLs needed for citation validation.

### Minimal Request Payload

```json
{
  "model": "sonar-pro",
  "messages": [
    {
      "role": "user",
      "content": "<your research query here>"
    }
  ]
}
```

---

## Query Formulation for Academic Sources

Well-formed queries produce higher-quality sources. Apply these rules:

1. **Use precise technical terminology** — name the exact concept: "scaled dot-product attention", "multi-head self-attention", "positional encoding", not "how transformers work".
2. **Specify a publication year range** — append `published between 2017 and 2024` or `after 2020` to filter stale pre-deep-learning results.
3. **Name specific authors or venues where known** — e.g., "Vaswani et al. attention mechanism NeurIPS 2017" or "ACL 2023 Hebrew NLP BiDi".
4. **Request peer-reviewed sources explicitly** — add "peer-reviewed journal or conference paper" to the query.
5. **Scope to the book topic** — every query must be relevant to Transformer architectures or Hebrew academic publishing.

### Example Queries

```
Vaswani 2017 attention is all you need transformer architecture peer-reviewed NeurIPS

BERT pre-training bidirectional transformers Devlin 2019 ACL peer-reviewed

Hebrew NLP natural language processing transformer models 2020 to 2024 conference paper
```

---

## Distinguishing Primary from Secondary Sources

| Source Type | Definition | Treatment |
|---|---|---|
| **Primary** | Peer-reviewed paper published at a conference (NeurIPS, ACL, EMNLP, ICML, ICLR) or journal (JMLR, TACL) | Include; generate a BibTeX entry |
| **Secondary** | Blog post, documentation page, arXiv preprint without peer review, Stack Overflow | Exclude from citation list; may be used for background context only |

If Perplexity returns a result without a venue or DOI, classify it as secondary and do not add it to `refs.bib`.

---

## CRITICAL: ResearcherAgent MUST Write New BibTeX Entries to `refs.bib`

The ResearcherAgent is the **sole owner** of `refs.bib`. Every paper it cites must be physically written to `latex_output/refs.bib` using `latex_writer_tool` in **`append`** mode before reporting results to downstream agents. A citation key that does not exist in `refs.bib` will render as `[?]` in the PDF — this is a zero-score outcome.

### Mandatory workflow:

1. Search Perplexity for real peer-reviewed papers matching the topic.
2. For each paper found, construct a complete `@article` or `@inproceedings` BibTeX entry.
3. Write EACH entry to `latex_output/refs.bib` via `latex_writer_tool` in **`append`** mode — NEVER `write` mode:
   ```
   path='latex_output/refs.bib', mode='append', content='@article{schick2023toolformer,\n  author  = {Schick, Timo and ...},\n  title   = {Toolformer: Language Models Can Teach Themselves to Use Tools},\n  journal = {NeurIPS},\n  year    = {2023}\n}\n\n'
   ```

   **CRITICAL: DO NOT USE `mode='write'` FOR `refs.bib`.**
   Using `mode='write'` DESTROYS all existing BibTeX entries (vaswani2017attention, brown2020language, wei2022chain, etc.) that ContentAgent chapters already depend on. This causes biber to fail with undefined references. If you use write mode, you will cause a zero-score bibliography section.

   The only allowed modes for `refs.bib` are:
   - `mode='append'` — ALWAYS use this to add new entries.
   - NEVER `mode='write'` for refs.bib regardless of whether the file exists or not.

4. Only AFTER writing to `refs.bib`, report the citation key to downstream agents.

### CRITICAL: Citation Keys MUST Be `author_year_keyword` — ALL LOWERCASE

**FORBIDDEN patterns that have caused zero-score bibliography sections:**

| Forbidden (NEVER use) | Why broken | Correct form |
|---|---|---|
| `Anthropic_2024_AgentArchitecture` | CapitalCase + org name ≠ author name | `anthropic2024agents` (only if a real paper) |
| `CrewAI_2024_HierarchicalDelegation` | CapitalCase + product name | `chase2022lmindex` (cite the actual paper) |
| `Stanford_MIT_2023_HierarchicalMultiAgentRL` | Institution names, not authors | `lowe2017multiagent` (cite the actual RL paper) |
| `OpenAI_2024_AgentsMCPIntegration` | Organization + product | `xi2023rise` (cite a real agents survey paper) |

The strict `author_year_keyword` pattern requires:
- `author`: first author's **last name**, all lowercase, no spaces (e.g., `schick`, `yao`, `brown`)
- `year`: four-digit year from the paper (e.g., `2023`, `2022`)
- `keyword`: one lowercase word from the paper title (e.g., `toolformer`, `react`, `language`)

### Authoritative paper list for multi-tool LLM agent topics:

If the research topic is about multi-tool orchestration or LLM agents, these real papers MUST be found and cited:

| Citation key | Paper | Venue |
|---|---|---|
| `schick2023toolformer` | Toolformer: Language Models Can Teach Themselves to Use Tools | NeurIPS 2023 |
| `yao2023react` | ReAct: Synergizing Reasoning and Acting in Language Models | ICLR 2023 |
| `xi2023rise` | The Rise and Potential of Large Language Model Based Agents: A Survey | arXiv 2023 |
| `park2023generative` | Generative Agents: Interactive Simulacra of Human Behavior | UIST 2023 |
| `shinn2023reflexion` | Reflexion: Language Agents with Verbal Reinforcement Learning | NeurIPS 2023 |
| `wei2022chain` | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models | NeurIPS 2022 |
| `brown2020language` | Language Models are Few-Shot Learners | NeurIPS 2020 |
| `vaswani2017attention` | Attention Is All You Need | NeurIPS 2017 |

Write ALL of these to `refs.bib` before reporting. Downstream ContentAgent will use these keys in `\cite{}` commands.

---

## Citation & Bibliography Guardrail

### NEVER cite the search tool or AI assistants as academic sources

The following are **forbidden citation sources** that must never appear in `refs.bib` or any `\cite{}` command:

| Forbidden entity | Why forbidden |
|---|---|
| Perplexity, Perplexity AI, sonar-pro | Perplexity is the **search tool**, not an academic author. Citing it is equivalent to citing Google Search. |
| OpenAI, Anthropic, Claude, ChatGPT (as a source, not a paper author) | AI assistants and their providers are not peer-reviewed academic sources unless you are citing a specific, named research paper with real authors and a real venue. |
| Any key matching `perplexity_YYYY_*` | This pattern is synthetic. Keys of this form are never valid BibTeX keys — they have no corresponding real paper. Reject every one. |

### Citation keys MUST follow `author_year_keyword` — derived from the real paper

Keys must be constructed from **the actual paper's metadata**, not from the tool used to find the paper:

```
CORRECT:   vaswani2017attention   devlin2019bert   touvron2023llama
FORBIDDEN: perplexity_2024_transformer   openai_2023_search   sonar_2024_nlp
```

The strict pattern is:
- **`author`** — first author's last name, lowercase, no spaces (e.g., `vaswani`, `devlin`, `touvron`)
- **`year`** — four-digit publication year from the paper itself (e.g., `2017`, `2019`)
- **`keyword`** — one lowercase word from the paper title (e.g., `attention`, `bert`, `llama`)

### Extraction workflow — cite the source, not the search engine

When Perplexity returns a result, extract citation metadata from the **source paper**, not from Perplexity's response envelope:

1. Locate the paper's DOI, arXiv ID, or conference proceedings URL in the Perplexity response.
2. Extract: full author list, full paper title, four-digit publication year, venue name.
3. Construct the BibTeX entry and citation key from those fields only.
4. Verify the venue is a recognised conference (NeurIPS, ACL, EMNLP, ICML, ICLR) or journal (JMLR, TACL).

### Minimum valid BibTeX entry

Every entry written to `refs.bib` must include all mandatory fields:

```bibtex
@article{vaswani2017attention,
  author  = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and
             Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and
             Kaiser, Łukasz and Polosukhin, Illia},
  title   = {Attention Is All You Need},
  journal = {Advances in Neural Information Processing Systems},
  year    = {2017},
  volume  = {30}
}
```

A BibTeX entry missing `author`, `title`, `year`, or `journal`/`booktitle` is invalid — do not write it to `refs.bib` until all mandatory fields are present and sourced from the real paper.

---

## Required Output Format

The Research Agent must return a single Markdown block. Each source occupies one entry with these fields:

```markdown
## Research Output

### [author_year_keyword]
- **Title:** Full paper title
- **Authors:** Last, F.; Last, F.
- **Year:** YYYY
- **Venue:** Conference or journal name
- **Summary:** First sentence describes the paper's main contribution. Second sentence explains its relevance to Transformer architectures or Hebrew NLP for this book.

### [author_year_keyword]
...
```

- **Citation key** (`author_year_keyword`) must follow the pattern: first author's last name + year + one lowercase keyword. Example: `vaswani2017attention`, `devlin2019bert`, `touvron2023llama`.
- **Minimum 6 entries** must be produced per research task.
- All citation keys produced here are used verbatim as BibTeX entry keys in `refs.bib` and `\cite{}` commands in chapter files.

---

## Two-Folder Wiki Memory Pattern

After collecting all sources, apply the wiki pattern to cut downstream token usage by ~95%:

### Folder layout (inside `latex_output/`)

| Path | Purpose |
|---|---|
| `raw/research_raw.md` | Verbatim Perplexity output — audit trail only, never passed to agents |
| `wiki/sources.md` | Distilled: one paragraph per source (citation key + contribution) |
| `wiki/index.md` | Index: one line per citation key with backlink to `wiki/sources.md` |

### Required sequence

1. **Save raw** — call `latex_writer_tool(path='raw/research_raw.md', content=<full Perplexity output>, mode='write')`.
2. **Distill** — write a concise paragraph per source (≤ 60 words each) into `wiki/sources.md`.
3. **Index** — write `wiki/index.md` with one line per citation key: `- [key](sources.md): <one-line description>`.
4. **Return output** — the task output must be ONLY the `wiki/sources.md` content. Do NOT return the raw dump.

Downstream agents (content writer) read only the distilled `wiki/` output via task context, never the raw files.

---

## Mapping to `refs.bib`

Every citation key in the research output must have a corresponding BibTeX entry written to `latex_output/refs.bib`. The Outline Agent will use these keys when populating the `refs` field of `book_outline.json`. The Content Agent will use them in `\cite{}` commands. Any key produced by the Researcher but missing from `refs.bib` will cause a Biber compilation error.

---

## Rate-Limit Handling

If the Perplexity API returns HTTP **429 Too Many Requests**:

1. **Do not propagate the error silently.** Re-raise `requests.HTTPError` with the 429 status so the Manager Agent's retry policy can handle it.
2. Wait before retrying — the Manager Agent applies exponential backoff via its retry policy (up to `MAX_AGENT_RETRIES` attempts).
3. Do not swallow the exception or return an empty result string.

For HTTP **4xx errors other than 429** (e.g., 401 Unauthorized, 400 Bad Request): raise `ValueError` with the status code and response body so the operator can diagnose the cause.

---

## Worked Example

### Query Sent to Perplexity

```
Vaswani 2017 attention transformer architecture peer-reviewed NeurIPS scaled dot-product multi-head
```

### Expected Response Block

```markdown
## Research Output

### vaswani2017attention
- **Title:** Attention Is All You Need
- **Authors:** Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A. N.; Kaiser, Ł.; Polosukhin, I.
- **Year:** 2017
- **Venue:** Advances in Neural Information Processing Systems (NeurIPS)
- **Summary:** Introduces the Transformer architecture based entirely on self-attention mechanisms, eliminating recurrence and convolution. This paper is the foundational reference for every chapter discussing attention and the encoder-decoder design in this book.

### devlin2019bert
- **Title:** BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
- **Authors:** Devlin, J.; Chang, M.-W.; Lee, K.; Toutanova, K.
- **Year:** 2019
- **Venue:** North American Chapter of the Association for Computational Linguistics (NAACL)
- **Summary:** Presents BERT, a bidirectional Transformer pre-trained on masked language modelling and next-sentence prediction. Relevant to the fine-tuning and applications chapter as the canonical example of transfer learning from Transformer representations.
```
