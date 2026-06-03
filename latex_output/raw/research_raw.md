# Raw Perplexity Research Output — Transformer Architectures & Hebrew NLP
## Audit File — Do Not Use Directly in Final Output
---

## Query 1: Transformer architecture attention mechanism self-attention peer-reviewed survey

The most widely cited peer-reviewed survey that specifically reviews **transformer/self-attention mechanisms** is *"Efficient Transformers: A Survey"* (Tay et al., 2020, ACM Computing Surveys), which systematically categorizes attention variants and efficiency techniques for Transformer architectures. In more domain-focused areas, key peer-reviewed surveys include *"Transformers in Vision: A Survey"* (Khan et al., ACM Computing Surveys, 2022) for computer vision and *"Transformer Architecture and Attention Mechanisms in Genome Analysis"* (Nguyen et al., 2023) for genomics.

### 1. General / Methodological surveys on Transformers & self-attention

1. **Efficient Transformers: A Survey** – Yi Tay, Mostafa Dehghani, et al., *ACM Computing Surveys*, 2020 (peer-reviewed journal)
   - Covers the **standard scaled dot-product self-attention** introduced in *Attention Is All You Need* and systematically reviews efficient variants (sparse, low-rank, kernelized, memory-compressed, etc.).
   - Widely used as the "go-to" reference when discussing **self-attention complexity** and architectural variants.

2. **A Survey on Efficient Training of Transformers** – (various authors, 2023)
   - Focuses on training-time issues (optimization, memory, parallelism).

### 2. Domain-specific transformer/self-attention surveys (peer-reviewed)

- **Vision:** **Transformers in Vision: A Survey** – Salman Khan et al., *ACM Computing Surveys*, 2022.
  - Reviews self-attention and Transformer architectures in computer vision, including Vision Transformers (ViT).

- **Genomics / Bioinformatics:** **Transformer Architecture and Attention Mechanisms in Genome Analysis** – Nguyen et al., 2023.
  - Comprehensive review of transformers and attention mechanisms applied to genome and sequence analysis.

### 3. Foundational transformer/self-attention references

- **Attention Is All You Need** – Vaswani et al., NeurIPS 2017 (peer-reviewed conference).
  - Introduces the **Transformer** and the **scaled dot-product self-attention** mechanism, along with **multi-head attention**.
  - Defines queries, keys, values, and the core attention computation.

---

## Query 2: Hebrew NLP natural language processing deep learning transformer models

Modern Hebrew NLP is built almost entirely on **Transformer-based deep learning models**, with several Hebrew-specific BERT/RoBERTa-style encoders.

### 1. Core Hebrew Transformer models

- **AlephBERT-base** (onlplab, BIU)
  - Architecture: same as English BERT-base (12 layers, 768 hidden, 12 heads, ~110M params).
  - Trained on large Hebrew corpora (~95M sentences from Twitter, Hebrew Wikipedia, OSCAR Hebrew).
  - Achieves **state-of-the-art** on morphological tagging, POS tagging, NER.

- **heBERT** (avichr)
  - Hebrew BERT, widely used in early Hebrew transformer work.
  - Variants: **Legal-heBERT** – Hebrew legal domain.

- **Dicta models (DictaBERT family):**
  - **DictaBERT**, **DictaBERT-large**, **NeoDictaBERT**, **NeoDictaBERT-bilingual (he-en)**

- **HeRo / LongHeRo** (HeNLP)
  - **HeRo** – Hebrew RoBERTa
  - **LongHeRo** – extended context length

### 2. Typical tasks handled with Hebrew Transformers

- Morphological analysis & POS tagging
- Named Entity Recognition (NER)
- Short answer grading / text classification
- Sentiment / topic classification
- Machine Translation (seq2seq)

### 3. Machine Translation and sequence-to-sequence for Hebrew

- A Harvard thesis implemented **Google's Transformer architecture** for Hebrew MT, beating Google Translate on in-genre Hebrew translation (METEOR scores).
- Deep learning work on **morphological parsing of Biblical Hebrew** uses both **LSTM** and **Transformer** models.

---

## Query 3: Vaswani "Attention is All You Need" Transformer NeurIPS 2017

The original *"Attention Is All You Need"* Transformer paper is by **Vaswani et al., 2017**, published at **NeurIPS 2017**.

- **Title:** Attention Is All You Need
- **Authors:** Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin
- **Conference:** 31st Conference on Neural Information Processing Systems (**NeurIPS 2017**), Long Beach, CA, USA
- **arXiv ID:** arXiv:1706.03762 (cs.CL)
- **Original submission date:** 12 June 2017

Core contribution:
- Introduces the **Transformer** architecture, a sequence transduction model **based solely on attention mechanisms**, dispensing with recurrence (RNNs) and convolutions (CNNs).
- Shows state-of-the-art results on WMT 2014 **English–German** and **English–French** machine translation.

---

## Query 4: BERT pre-training deep bidirectional transformers language understanding Devlin 2019

- **Title:** BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
- **Authors:** Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova
- **Venue:** Proceedings of NAACL-HLT 2019 (Volume 1: Long Papers)
- **Year:** 2019
- **Pages:** 4171–4186
- **DOI:** 10.18653/v1/N19-1423
- **arXiv ID:** arXiv:1810.04805

---

## Query 5: AlephBERT Hebrew BERT morphological analysis Ben-David 2022

**AlephBERT** is a Hebrew BERT-style model introduced by **Seker, Greenfeld & Shwartz (ACL 2022)**.

- **Model type:** BERT-base style Hebrew PLM: 12 layers, 768 hidden size, 12 heads, ~110M params.
- **Vocabulary & data:** ~52K wordpiece vocab, trained on ~95M sentences from Hebrew OSCAR, Hebrew Wikipedia, and Twitter.
- **Novel morphological extraction architecture** on top of AlephBERT's contextual embeddings.
- **Results:** AlephBERT-base achieves new state-of-the-art for Hebrew on morphological segmentation, POS tagging, full morphological tagging, dependency parsing, NER, and sentiment analysis.
- **Model & code:** GitHub `OnlpLab/AlephBERT`; HuggingFace `onlplab/alephbert-base`.

---

## Query 6: FlashAttention efficient exact attention IO-complexity Dao 2022

**FlashAttention** (Dao et al., 2022) is an **exact attention** algorithm designed to be **IO-aware**.

Key IO-complexity result:
- FlashAttention needs **O(N^2 d^2 / M)** HBM accesses (N = sequence length, d = head dimension, M = SRAM size).
- Standard attention requires **Ω(Nd + N^2)** HBM accesses.
- Does not materialize the full N×N attention matrix in HBM.
- Stores only small softmax statistics and recomputes intermediates during backward pass.
- Reported practical impact: up to **7.6× speedup** on GPT-2 attention, up to **9× fewer HBM accesses**.

---

## Query 7: Tay efficient transformers survey ACM Computing Surveys 2022

- **Title:** Efficient Transformers: A Survey
- **Authors:** Yi Tay, Mostafa Dehghani, Dara Bahri, Donald Metzler
- **Venue:** ACM Computing Surveys (CSUR), 2022
- **arXiv v2:** "2022 edition"

Main categories of efficient attention variants:
- **Low-rank / projection-based:** Linformer – projects K/V from N×d to k×d, reducing to O(Nk).
- **Kernel / random feature–based:** Performer – approximates softmax with kernel random features, O(Ld^2).
- **Clustered / routing-style:** Clustered attention – cluster queries, attend via centroids.
- **Local / sparse / block-sparse:** Longformer, BigBird – combine global, sliding-window, random attention patterns.
- **LSH-based:** Reformer – locality-sensitive hashing attention, O(N log N) memory.

---

## Query 8: Rotary Position Encoding RoPE Su 2021

**Rotary Position Embedding (RoPE)** introduced by **Su et al. 2021** in the *RoFormer* paper.

Core idea:
- Encodes positions by applying position-dependent 2D rotations to query and key vectors.
- Attention depends on **relative** positions; parameter-free.
- For positions p and q: Q̃_p^T K̃_q = Q_p^T R_{q-p} K_q — attention logit depends on (q−p).

Properties:
- **Parameter-free:** No additional learned parameters.
- **Relative position explicit** in the dot product via angle differences.
- **Flexible sequence length:** Can generalize beyond training length.
- **Kernel-friendly:** Works well with FlashAttention.
- Widely adopted in modern LLMs (LLaMA family).

- **Paper:** RoFormer: Enhanced Transformer with Rotary Position Embedding – Jianlin Su et al., 2021.

---
*End of raw Perplexity dump. For audit purposes only.*
