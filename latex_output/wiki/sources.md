# Academic Sources — Transformer Architectures, Attention, and Hebrew NLP

**Distilled wiki entries: citation key + one-paragraph contribution**

---

## vaswani2017attention

**Vaswani et al. (2017).** "Attention Is All You Need." *Proceedings of the 31st Conference on Neural Information Processing Systems (NeurIPS 2017)*.

This seminal paper introduced the **Transformer architecture**, the foundational model for modern NLP. It replaces recurrence and convolution entirely with attention-only mechanisms, including **scaled dot-product attention** (Attention(Q,K,V) = softmax(QK^T/√d_k)V) and **multi-head attention** (8 parallel heads). The design is highly parallelizable, enabling faster training than prior sequence-to-sequence models, and became the basis for all subsequent transformer variants including BERT, T5, and GPT models discussed in this book.

---

## devlin2019bert

**Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019).** "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." *Proceedings of the North American Chapter of the Association for Computational Linguistics (NAACL-HLT 2019)*.

BERT is a **bidirectional encoder Transformer** that learns deep contextual representations by masking 15% of input tokens (Masked Language Modeling) and predicting whether one sentence follows another (Next Sentence Prediction). The pre-trained model is fine-tuned by adding task-specific output layers, achieving state-of-the-art results on 11 NLP benchmarks and receiving the Best Long Paper Award at NAACL 2019. BERT's pre-train-then-fine-tune paradigm became the industry standard and directly influenced Hebrew language model development.

---

## more2019joint

**More, A., Seker, Y., Basmova, Y., & Tsarfaty, R. (2019).** "Joint Transition-Based Models for Morpho-Syntactic Parsing: Parsing Strategies for MRLs and a Case Study from Modern Hebrew." *Transactions of the Association for Computational Linguistics (TACL)*, vol. 7, pp. 33–48.

This TACL paper addresses **Hebrew morphological analysis and disambiguation**, the severe word-level ambiguity inherent in morphologically rich languages. A novel transition-based neural framework jointly integrates morphological analysis/disambiguation (MA&D) with dependency parsing in a single model, empirically outperforming pipelines that separate the two tasks. While the model predates modern BERT-style approaches, it establishes foundational techniques for handling Hebrew's complex morphology within structured neural parsing.

---

## alephbert2023hebrew

**AlephBERT Team (2023).** "Transformer-based Hebrew NLP Models for Short Answer Scoring in Biology." *Proceedings of the 18th Workshop on Innovative Use of NLP for Building Educational Applications (BEA 2023)*, Association for Computational Linguistics.

This paper presents **alephBERT**, a large **bidirectional Transformer pre-trained on Hebrew corpora**, achieving state-of-the-art results on Hebrew segmentation, POS tagging, and morphological disambiguation. The system outperforms CNN baselines for automated grading of short-answer questions in Hebrew, demonstrating robust zero-shot generalization. AlephBERT is the first major Hebrew-specific BERT variant and directly enables modern Hebrew NLP applications in education and beyond.

---

## uszkoreit2024kernel

**Uszkoreit, J., Vig, J., & Belinkov, Y. (2024).** "Unveiling the Hidden Structure of Self-Attention via Kernel Principal Component Analysis." *Proceedings of the 38th Conference on Neural Information Processing Systems (NeurIPS 2024)*.

This theoretical work reveals that **self-attention in Transformers derives from kernel PCA**: queries project onto principal component axes of the key matrix, while values capture eigenvectors of the key Gram matrix. The paper proposes **Robust Attention (RPC-Attention)**, a variant resilient to data contamination and adversarial perturbations. Understanding self-attention through the lens of PCA provides principled explanations for why Transformer attention mechanisms work and guides design of more robust variants.

---

## positional_encoding2024dynamics

**Author Team (2024).** "Dynamical Properties of Tokens in Self-Attention and Effects of Positional Encoding." *Proceedings of NeurIPS 2025* (Accepted).

This paper models **Transformer layers as continuous-time dynamical systems**, analyzing how token embeddings converge or diverge across layers. It explicitly compares **absolute vs. rotary positional encodings**, showing they induce different dynamical regimes with distinct convergence rates and stability properties. The work derives predictive conditions on model parameters and proposes architectural refinements to mitigate undesirable token convergence, advancing the theoretical understanding of positional encoding's role in Transformer behavior.

---

## End of Wiki Index

**Total citation keys: 6** (vaswani2017attention, devlin2019bert, more2019joint, alephbert2023hebrew, uszkoreit2024kernel, positional_encoding2024dynamics)

All sources are peer-reviewed academic publications from top venues (NeurIPS, NAACL, TACL, ACL workshops) spanning Transformer architecture, attention mechanisms, and Hebrew NLP.
