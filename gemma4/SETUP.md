# Gemma 4 Local Deployment Guide

## Overview

Gemma 4 26B-A4B is a Mixture-of-Experts model with 25.2B total params but only ~4B active per token. It runs on consumer GPUs with Vulkan acceleration via `llama.cpp`.

## Requirements

- **RAM:** 16GB minimum
- **VRAM:** 8GB+ recommended (Vulkan GPU)
- **Storage:** ~16GB for Q4_K_M quantization
- **OS:** Windows, Linux, macOS

## Install llama.cpp

```bash
# Windows (winget)
winget install ggml.llamacpp

# macOS (Homebrew)
brew install llama.cpp

# Linux (build from source)
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp && cmake -B build && cmake --build build --config Release
```

## Start the Server

```bash
# Chat/Inference mode
llama-server \
  -hf ggml-org/gemma-4-26b-a4b-it-GGUF:Q4_K_M \
  --port 8080

# With thinking mode enabled (default for Gemma 4)
# The server auto-detects the chat template with thinking=1
```

## Test Inference

```bash
curl -s http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-4",
    "messages": [{"role": "user", "content": "Explain MRL in 3 sentences."}]
  }' | python -m json.tool
```

## Embeddings

> **Important:** For embeddings, use `EmbeddingGemma-300M` via `sentence-transformers` instead of the generative model. The generative model's embedding endpoint is unstable due to session management and VRAM constraints.

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("google/embeddinggemma-300M")

# For indexing documents
doc_embeddings = model.encode(
    documents,
    prompt_name="Retrieval-document",
    truncate_dim=768,
    normalize_embeddings=True
)

# For search queries
query_embedding = model.encode(
    "your search query",
    prompt_name="Retrieval-query",
    truncate_dim=768,
    normalize_embeddings=True
)
```

## Cognitive Stratification

| Layer | Model | Use Case | Cost |
|---|---|---|---|
| **Architect** | Gemini 3.1 Pro (Cloud) | Complex synthesis, multi-file refactoring | API pricing |
| **Worker Bee** | Gemma 4 26B-A4B (Local) | High-volume code gen, sensitive data, offline | $0 |
| **Librarian** | EmbeddingGemma-300M (Local) | Semantic search, RAG retrieval | $0 |

## Key Specs

| Parameter | Value |
|---|---|
| Architecture | Mixture of Experts (MoE) |
| Total Params | 25.2B |
| Active Params | ~4B per token |
| Experts | 128 total, 8 active |
| Context | 128K (expandable to 256K) |
| Quantization | Q4_K_M (~16GB) |
| Thinking Mode | Built-in (1.1K token budget) |
| Function Calling | Native Action-Observation objective |
