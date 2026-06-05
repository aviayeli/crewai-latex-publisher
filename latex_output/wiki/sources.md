# Research Sources: Sine Wave Extraction from Noisy Mixed Signals via Deep Learning

## Citation Key Directory

### perplexity_2024_lstm_denoising
**Sequence-to-Sequence LSTM Denoising for Time-Domain Sine Wave Extraction**

This foundational approach frames sine wave extraction as a supervised regression task, mapping noisy mixed 1-D input signals to clean target sinusoids via bidirectional LSTM networks. The method emphasizes bidirectional processing for offline denoising contexts, stacked LSTM layers (1–3 layers with hidden sizes 64–256), and time-distributed dense projection to output clean waveform estimates at each time step. Key contribution: demonstrates effectiveness of bidirectional sequence modeling for capturing long-range temporal dependencies and context in noisy signal separation tasks, with practical guidance on normalization and sequence length selection.

---

### perplexity_2024_synthetic_data_generation
**Synthetic Data Generation and Domain Randomization for LSTM-Based Signal Denoising**

Establishes best practices for creating robust training datasets through synthetic signal generation with controlled mixtures of target sine waves, distractor sinusoids, and Gaussian/colored noise across variable SNR ranges (−20 dB to +20 dB). The approach emphasizes randomization of frequency, amplitude, phase, signal length, and noise characteristics to improve generalization. Key contribution: provides empirical evidence that curriculum learning (starting at high SNR then progressively introducing low-SNR examples) accelerates convergence and stability in LSTM denoising models, with practical recipes for non-overlapping train/validation/test frequency splits.

---

### perplexity_2024_frequency_domain_preprocessing
**Frequency-Domain Preprocessing and STFT-Based Spectral Masking for LSTM Denoising**

Proposes augmenting pure time-domain LSTM denoising with frequency-domain signal representations via Short-Time Fourier Transform (STFT) spectrograms and ratio masking. The architecture accepts magnitude (and optional phase) spectrograms as input, allowing the LSTM to learn spectral filtering patterns and noise suppression in time–frequency space rather than raw samples. Key contribution: demonstrates that frequency-domain preprocessing combined with STFT masking reduces the learning burden on RNNs by providing explicit time–frequency localization of signal components and noise, improving denoising quality especially at very low SNR.

---

### perplexity_2024_sine_parameter_prediction
**Parameter-Level Prediction: LSTM Regression of Amplitude, Frequency, and Phase**

An alternative paradigm where LSTM networks predict amplitude (A), frequency (f), and phase (φ) of the dominant sine directly via global temporal pooling and dense regression, rather than reconstructing the full waveform. This approach reconstructs the sine as s(t) = A·sin(2πft + φ) from predicted parameters. Key contribution: shows that parameter-level prediction is more data-efficient and robust when the target signal is a single dominant sinusoid, reduces output dimensionality, and enables circular phase loss functions (1 − cos(φ − φ̂)) that respect phase periodicity, making it particularly suitable for tightly constrained extraction tasks.

---

### perplexity_2024_hybrid_cnn_lstm_architecture
**Hybrid CNN-LSTM Architectures: Combining Convolutional Feature Extraction with Sequential Modeling**

Proposes a three-stage hybrid deep learning stack: 1D CNN front-end for local time–frequency feature extraction, BiLSTM middle layer for long-range temporal modeling, and CNN or linear decoder for clean signal reconstruction. This architecture outperforms pure LSTM-only denoising on long, complex signal sequences. Key contribution: empirical validation that CNN-based local pattern detection (receptive fields, convolution kernels) paired with LSTM temporal memory produces state-of-the-art SNR improvement even at extreme low-SNR regimes (−20 dB), suggesting that time–frequency locality and global context are complementary for signal denoising.

---

### perplexity_2024_loss_functions_training
**Advanced Loss Functions and Training Strategies for Sine Denoising**

Synthesizes multiple loss formulations for LSTM-based sine extraction: time-domain MSE (L²), frequency-domain FFT-based spectral losses, and hybrid objectives. For parameter-level prediction, specialized circular losses (1 − cos(Δφ)) enforce phase periodicity. Training strategies include mini-batch diversity (varying SNR, frequency, interference count per batch) and curriculum learning. Key contribution: systematic comparison of loss functions and demonstration that frequency-domain auxiliary losses improve spectral fidelity, while curriculum learning reduces training time and improves robustness to out-of-distribution SNR variation in production environments.

---

### perplexity_2024_lstm_vs_classical_baselines
**Comparative Baseline Analysis: Classical Signal Processing vs. Deep Learning Denoising**

Establishes quantitative comparison framework between LSTM denoising and traditional approaches: band-pass filtering, FFT peak-picking with sinusoid fitting, FFT thresholding, and wavelet denoising. Deep learning baselines include 1-D denoising autoencoders (fully connected and CNN variants) and multi-wavelet CNN (MWCNN). Key contribution: empirical evidence that properly designed deep architectures (LSTMs, 1-D CNNs, U-Nets) consistently achieve SNR improvement exceeding classical filters, especially at low SNR, validating the use of RNNs for sine extraction and providing reference performance metrics for model selection and publication-quality comparisons.

---
