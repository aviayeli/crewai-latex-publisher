# wiki/index.md — Citation Index
## Transformer Architectures, Attention Mechanisms, and Hebrew NLP
---

| Citation Key | One-Line Description | Source |
|---|---|---|
| `vaswani_2017_transformer` | Introduces the original Transformer architecture with scaled dot-product and multi-head self-attention, replacing RNNs/CNNs entirely. | [wiki/sources.md](wiki/sources.md#vaswani_2017_transformer) |
| `devlin_2019_bert` | Presents BERT's bidirectional pre-training via masked language modeling, establishing the pre-train-then-fine-tune paradigm for NLP. | [wiki/sources.md](wiki/sources.md#devlin_2019_bert) |
| `tay_2022_efficient_transformers` | Comprehensive ACM survey taxonomizing efficient Transformer variants (Linformer, Performer, Longformer, Reformer, BigBird) by complexity reduction strategy. | [wiki/sources.md](wiki/sources.md#tay_2022_efficient_transformers) |
| `seker_2022_alephbert` | Introduces AlephBERT, the canonical Hebrew BERT model achieving state-of-the-art on morphological segmentation, POS, NER, and parsing. | [wiki/sources.md](wiki/sources.md#seker_2022_alephbert) |
| `dao_2022_flashattention` | Presents FlashAttention, an IO-aware exact attention algorithm achieving O(N²d²/M) HBM accesses and up to 7.6× speedup over standard attention. | [wiki/sources.md](wiki/sources.md#dao_2022_flashattention) |
| `su_2021_rope` | Introduces RoPE (Rotary Position Embedding), a parameter-free relative positional encoding widely adopted in modern LLMs including LLaMA. | [wiki/sources.md](wiki/sources.md#su_2021_rope) |
| `tsarfaty_2020_hebrew_ud` | Establishes Hebrew UD treebank standards and morphosyntactic evaluation frameworks essential for benchmarking Hebrew NLP Transformer models. | [wiki/sources.md](wiki/sources.md#tsarfaty_2020_hebrew_ud) |

---

## Quick Navigation

- **Full source descriptions with one-paragraph summaries:** [wiki/sources.md](wiki/sources.md)
- **Raw Perplexity API output (audit only):** [raw/research_raw.md](raw/research_raw.md)

---

## Coverage Summary

- **Foundational architecture:** `vaswani_2017_transformer`, `devlin_2019_bert`
- **Efficiency & hardware optimization:** `tay_2022_efficient_transformers`, `dao_2022_flashattention`
- **Positional encoding:** `su_2021_rope`
- **Hebrew NLP:** `seker_2022_alephbert`, `tsarfaty_2020_hebrew_ud`

*7 sources total — exceeds the minimum requirement of 6 citation-ready sources.*
