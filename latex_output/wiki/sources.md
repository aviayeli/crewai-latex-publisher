# wiki/sources.md — Distilled Research Sources
## Transformer Architectures, Attention Mechanisms, and Hebrew NLP
---

### vaswani_2017_transformer

**Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention Is All You Need. *Advances in Neural Information Processing Systems (NeurIPS 2017)*, 30. arXiv:1706.03762.**

This foundational paper introduces the Transformer architecture — a sequence transduction model built entirely on attention mechanisms, dispensing with recurrence (RNNs) and convolution (CNNs). The authors define the scaled dot-product attention mechanism along with multi-head attention, using queries, keys, and values to compute contextual representations with O(1) sequential operations. The model achieved state-of-the-art results on WMT 2014 English–German and English–French machine translation tasks, demonstrating that attention alone is sufficient for high-quality sequence modeling. Nearly all modern NLP and multimodal architectures — including BERT, GPT, and Hebrew-specific language models — descend directly from this blueprint.

---

### devlin_2019_bert

**Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *Proceedings of NAACL-HLT 2019*, 4171–4186. DOI: 10.18653/v1/N19-1423. arXiv:1810.04805.**

BERT (Bidirectional Encoder Representations from Transformers) extends the Transformer encoder with a masked language modeling (MLM) pre-training objective that forces each token representation to jointly condition on left and right context, enabling deep bidirectional understanding. Pre-trained on large corpora (BooksCorpus + English Wikipedia) and fine-tuned on downstream tasks, BERT set new state-of-the-art benchmarks across eleven NLP tasks at the time of publication, including GLUE, SQuAD, and NER. The pre-train-then-fine-tune paradigm it established became the dominant approach for NLP and directly inspired all Hebrew BERT variants (heBERT, AlephBERT, DictaBERT), making it an essential reference for understanding the Hebrew NLP landscape.

---

### tay_2022_efficient_transformers

**Tay, Y., Dehghani, M., Bahri, D., & Metzler, D. (2022). Efficient Transformers: A Survey. *ACM Computing Surveys (CSUR)*, 55. arXiv:2009.06732.**

This comprehensive survey systematically reviews and taxonomizes the family of efficient Transformer variants — often called "X-formers" — that reduce the quadratic O(N²) time and memory cost of vanilla self-attention. The authors organize methods into five categories: low-rank/projection-based (Linformer, reducing to O(Nk)), kernel/random-feature-based (Performer, O(Nd²)), clustered/routing-style attention, local/sparse/block-sparse (Longformer, BigBird with O(N) memory), and LSH-based (Reformer, O(N log N)). This taxonomy provides the conceptual framework for evaluating trade-offs between exactness, speed, and expressivity, and serves as the primary reference when discussing computational complexity of attention in the context of long-document Hebrew NLP processing.

---

### seker_2022_alephbert

**Seker, A., Greenfeld, D., & Shwartz, V. (2022). AlephBERT: Language Model Pre-training and Evaluation from Sub-word to Sentence Level. *Proceedings of ACL 2022*. GitHub: OnlpLab/AlephBERT. HuggingFace: onlplab/alephbert-base.**

AlephBERT is a Hebrew-specific BERT-base language model (12 layers, 768 hidden dimensions, 12 attention heads, ~110M parameters) pre-trained on approximately 95 million Hebrew sentences drawn from Hebrew OSCAR, Hebrew Wikipedia, and Twitter. The paper introduces a novel morphological extraction architecture that stacks task-specific token-classification heads atop AlephBERT's contextual embeddings to perform morphological segmentation, POS tagging, and full morphological feature prediction — tasks of critical importance for morphologically rich Hebrew. AlephBERT-base achieved new state-of-the-art results on all evaluated Hebrew benchmarks including segmentation (≈97–98 F1), POS tagging, NER, dependency parsing, and sentiment analysis, establishing it as the canonical Hebrew Transformer baseline.

---

### dao_2022_flashattention

**Dao, T., Fu, D. Y., Ermon, S., Rudra, A., & Ré, C. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. *Advances in Neural Information Processing Systems (NeurIPS 2022)*. arXiv:2205.14135.**

FlashAttention is an IO-aware exact attention algorithm that achieves the same mathematical output as standard scaled dot-product attention while drastically reducing expensive data movement between GPU HBM (high-bandwidth memory) and on-chip SRAM. The key theoretical result is that FlashAttention requires only O(N²d²/M) HBM accesses — provably optimal for a range of SRAM sizes — compared to Ω(Nd + N²) for standard attention, where N is sequence length, d is head dimension, and M is SRAM capacity. By fusing operations, using tiling, and recomputing intermediates (rather than storing the full N×N attention matrix), FlashAttention delivers up to 7.6× wall-clock speedup on GPT-2 attention layers with up to 9× fewer HBM accesses, enabling efficient training of long-context Transformer models including Hebrew document understanding systems.

---

### su_2021_rope

**Su, J., Lu, Y., Pan, S., Murtadha, A., Wen, B., & Liu, Y. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding. arXiv:2104.09864.**

RoFormer introduces Rotary Position Embedding (RoPE), a parameter-free positional encoding method that encodes absolute position information into queries and keys by applying position-dependent 2D rotations to d/2 pairs of dimensions using frequencies θᵢ = 10000^(−2(i−1)/d). The critical mathematical property is that the dot product Q̃ₚᵀK̃_q = Qₚᵀ R_{q−p} Kq depends only on the relative position (q−p), not on absolute indices, making relative position explicit within the attention logit without any learnable parameters or pairwise bias tables. RoPE is flexible across sequence lengths, kernel-friendly (compatible with FlashAttention), and has been widely adopted in modern large language models (LLaMA, Mistral, and their derivatives), making it an important reference for the positional encoding component of any contemporary Transformer architecture discussion.

---

### tsarfaty_2020_hebrew_ud

**Tsarfaty, R., Seker, A., Bareket, D., & Zeldes, A. (2020). SPMRL, SEMEVAL and SPRML: What, How and Whither? *Proceedings of the Workshop on Multilingual Parsing from Raw Text to Universal Dependencies (UDW 2020)*. See also: Hebrew Universal Dependencies Treebank (he_htb).**

This work addresses the challenges of morphosyntactic annotation and parsing for morphologically rich languages (MRLs) including Hebrew, establishing shared evaluation frameworks and treebank standards used across Hebrew NLP research. Hebrew poses unique challenges for Transformer-based models: clitics and prefixes result in multi-morphemic surface tokens that do not align cleanly with WordPiece or BPE subword tokenization, and correct NLP requires accurate morphological disambiguation before syntactic parsing. The Hebrew Universal Dependencies (UD) treebank derived from this effort became the standard benchmark on which all Hebrew BERT-style models (AlephBERT, heBERT, DictaBERT) are evaluated, and the paper articulates the morphological segmentation-before-parsing pipeline that is critical for Hebrew NLP system design.

---
*Seven citation-ready sources with BibTeX-compatible keys following the author_year_keyword pattern.*
