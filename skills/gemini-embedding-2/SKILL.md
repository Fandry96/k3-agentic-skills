---
name: gemini-embedding-2
description: >
  Gemini Embedding 2 — Google's natively multimodal embedding model (GA April 2026).
  Maps text, images, video, audio, and PDFs into a unified 3072-dim vector space with
  MRL support (truncate to 128-3072). Use when: embeddings, semantic search,
  RAG, clustering, classification, multimodal retrieval, vector database,
  MRL truncation, cosine similarity, narrative memory, code retrieval,
  cross-modal search, agentic RAG.
---

# Gemini Embedding 2 — Skill Reference

> **Model:** `gemini-embedding-2` (stable) / `gemini-embedding-2-flash` (speed-optimized)
> **Released:** March 10, 2026 (Preview) → April 22, 2026 (GA)
> **Replaces:** `gemini-embedding-001`, `text-embedding-005`, `text-embedding-004`
> **Docs:** https://ai.google.dev/gemini-api/docs/embeddings
> **Source:** Deep Research synthesis (28 sources, May 2026)

---

## 1. Model Specifications

| Property | Value |
|---|---|
| **Model ID** | `gemini-embedding-2` |
| **Flash Variant** | `gemini-embedding-2-flash` (speed-optimized) |
| **Pinned Variant** | `gemini-embedding-2-flash-001` (reproducible vectors) |
| **Default Dimensions** | 3072 (float32) |
| **MRL Range** | 128, 256, 512, 768, 1536, 3072 |
| **Recommended MRL** | 3072 (max quality), 1536 (balanced), 768 (fast/cheap sweet spot) |
| **Max Text Tokens** | 8,192 (4× increase over text-embedding-004's 2,048) |
| **Max Images** | 6 per request (PNG, JPEG, WebP, BMP) |
| **Max Video** | 120s without audio / 80s with audio (MP4, MPEG, MOV) |
| **Max Audio** | 180 seconds native (MP3, WAV — no transcription needed) |
| **Max PDF** | 6 pages per file (integrated OCR) |
| **Languages** | 100+ |
| **Multimodal** | ✅ Natively multimodal — single transformer backbone, not stitched encoders |
| **Distance Metric** | Cosine Similarity (recommended) |

### MTEB Benchmarks

| Benchmark | Score | vs OpenAI 3-Large | vs text-embedding-004 |
|---|---|---|---|
| **MTEB English** | **68.32** | +3.72 (64.6) | +4-6 points |
| **MTEB Code** | **84.0** | — | — |
| **MTEB Multilingual** | **69.9** | — | — |
| **Video Retrieval (Vatex/MSR-VTT)** | **68.8** | N/A | N/A |

---

## 2. Pricing

| Platform | Tier | Text/Image/Video | Audio | Output |
|---|---|---|---|---|
| **AI Studio** | Free | $0.00 (rate-limited) | $0.00 | $0.00 |
| **AI Studio** | Paid | $0.20 / 1M tokens | $0.50 / 1M tokens | $0.00 |
| **Vertex AI** | Paid | $0.20 / 1M tokens | $0.50 / 1M tokens | $0.00 |
| **Batch API** | Indexing | ~$0.10 / 1M tokens | — | $0.00 |

### Cost Calculator

| Corpus Size | Est. Tokens | Cost |
|---|---|---|
| 100 docs × 2K tokens | 200K | $0.04 |
| 1,000 docs × 4K tokens | 4M | $0.80 |
| K3 MRL index (6,296 chunks) | ~12M | $2.40 |
| Proto_book full rebuild | ~20M | $4.00 |

---

## 3. Critical Breaking Change: Task Prefixes Replace task_type

**Gemini Embedding 2 does NOT use the `task_type` API parameter.** You MUST include task instructions as string prefixes in the content itself.

### Old Way (001) — DEPRECATED:
```python
config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
```

### New Way (embedding-2) — MANDATORY:
```python
# Prefix is part of the content string itself
content = "task: search result | query: western romance with grumpy hero"
```

---

## 4. Task Prefix Reference

### 4.1 Asymmetric Tasks (query ≠ document format)

Use different formats for queries vs documents. This is critical for retrieval/RAG.

| Task | Query Side | Document Side |
|---|---|---|
| **Search / RAG** | `task: search result \| query: {q}` | `title: {title} \| text: {content}` |
| **Q&A** | `task: question answering \| query: {q}` | `title: {title} \| text: {content}` |
| **Fact Check** | `task: fact checking \| query: {q}` | `title: {title} \| text: {content}` |
| **Code Search** | `task: code retrieval \| query: {q}` | `title: {title} \| text: {content}` |

> If document has no title, use `title: none | text: {content}`.

### 4.2 Symmetric Tasks (same format both sides)

| Task | Both Sides |
|---|---|
| **Classification** | `task: classification \| query: {content}` |
| **Clustering** | `task: clustering \| query: {content}` |
| **Similarity** | `task: sentence similarity \| query: {content}` |

### Helper Functions (Python)

```python
# Asymmetric retrieval
def prepare_query(query, task="search result"):
    return f"task: {task} | query: {query}"

def prepare_document(content, title=None):
    t = title or "none"
    return f"title: {t} | text: {content}"

# Symmetric
def prepare_symmetric(content, task="clustering"):
    return f"task: {task} | query: {content}"
```

---

## 5. Code Examples

### 5.1 Python — Basic Embedding

```python
from google import genai

client = genai.Client()  # Uses GEMINI_API_KEY env var

result = client.models.embed_content(
    model="gemini-embedding-2",
    contents="What is the meaning of life?"
)

vector = result.embeddings[0].values  # 3072 floats
```

### 5.2 Python — MRL Truncation (768 dims)

```python
from google import genai
from google.genai import types

client = genai.Client()

result = client.models.embed_content(
    model="gemini-embedding-2",
    contents="Ryder leaned against the fence post, jaw tight.",
    config=types.EmbedContentConfig(
        output_dimensionality=768  # MRL truncation — API normalizes for you
    )
)

vector = result.embeddings[0].values  # 768 floats, pre-normalized
```

### 5.3 Python — Asymmetric Search with Prefixes

```python
from google import genai
from google.genai import types
import numpy as np

client = genai.Client()

# Query side — uses task prefix
query = "task: search result | query: ranch romance with grumpy cowboy"
q_result = client.models.embed_content(
    model="gemini-embedding-2",
    contents=query,
    config=types.EmbedContentConfig(output_dimensionality=768)
)
q_vec = np.array(q_result.embeddings[0].values, dtype=np.float32)

# Document side — uses title/text prefix
docs = [
    "title: Flawless | text: Small-town western romance, grumpy cowboy mechanic...",
    "title: Ice Planet Barbarians | text: Sci-fi alien romance, survival...",
    "title: Heartless | text: Single dad rancher, woman next door...",
]
d_result = client.models.embed_content(
    model="gemini-embedding-2",
    contents=docs,
    config=types.EmbedContentConfig(output_dimensionality=768)
)

# Rank by cosine similarity
for i, emb in enumerate(d_result.embeddings):
    d_vec = np.array(emb.values, dtype=np.float32)
    score = np.dot(q_vec, d_vec) / (np.linalg.norm(q_vec) * np.linalg.norm(d_vec))
    print(f"{score:.4f}  {docs[i][:60]}")
```

### 5.4 Python — Multimodal (Image + Text)

```python
from google import genai
from google.genai import types

client = genai.Client()

# Embed image + text together as interleaved content
image_part = types.Part.from_uri(
    file_uri="gs://bucket/cover.jpg",
    mime_type="image/jpeg"
)

result = client.models.embed_content(
    model="gemini-embedding-2",
    contents=types.Content(parts=[
        types.Part(text="Romance novel cover with cowboy"),
        image_part
    ]),
    config=types.EmbedContentConfig(output_dimensionality=768)
)
```

### 5.5 JavaScript — Node.js (@google/genai)

```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

// Single embedding
const response = await ai.models.embedContent({
    model: "gemini-embedding-2",
    contents: "task: search result | query: western romance",
    config: { outputDimensionality: 768 }
});
const vector = response.embeddings[0].values;  // 768 floats

// Batch embedding
const batchResponse = await ai.models.embedContent({
    model: "gemini-embedding-2",
    contents: [
        "title: Flawless | text: A grumpy cowboy mechanic...",
        "title: Heartless | text: A single dad rancher...",
    ],
    config: { outputDimensionality: 768 }
});
```

### 5.6 REST API — cURL

```bash
# Single embedding
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:embedContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: ${GEMINI_API_KEY}" \
  -d '{
    "model": "models/gemini-embedding-2",
    "content": {
      "parts": [{"text": "task: search result | query: western romance"}]
    }
  }'

# Batch embedding
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:batchEmbedContents" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: ${GEMINI_API_KEY}" \
  -d '{
    "model": "models/gemini-embedding-2",
    "requests": [
      {"model": "models/gemini-embedding-2", "content": {"parts": [{"text": "doc 1"}]}},
      {"model": "models/gemini-embedding-2", "content": {"parts": [{"text": "doc 2"}]}}
    ]
  }'
```

---

## 6. MRL Strategy Guide

### Dimension Selection

| Use Case | Dims | Storage (1M vecs) | Quality |
|---|---|---|---|
| Mobile/edge | 256 | 1 GB | Good for coarse filtering |
| **Narrative memory (sqlite-vec)** | **768** | **3 GB** | **Sweet spot — near-peak quality** |
| MRL index (K3 skill search) | 768 | 3 GB | Fast local queries |
| Production RAG | 1536 | 6 GB | High quality |
| Max precision | 3072 | 12 GB | Full resolution |

### Two-Stage Retrieval Pattern

```
Phase 1 (Fast):  768D vectors → scan full index → top-K candidates
Phase 2 (Precise): 3072D vectors → rerank top-K only → final results
```

### L2 Normalization

When using `output_dimensionality` API parameter: **vectors are pre-normalized**.
When truncating client-side with numpy: **you must normalize manually**:

```python
import numpy as np

def truncate_and_normalize(vec_raw, dim=768):
    vec = np.array(vec_raw, dtype=np.float32)[:dim]
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec
```

---

## 7. Migration from Legacy Models

### Incompatibility Warning

Vectors from different models are **NOT compatible**. You cannot compare:
- `gemini-embedding-001` vectors with `gemini-embedding-2` vectors
- `text-embedding-004` vectors with `gemini-embedding-2` vectors

**Full re-indexing is required.**

### Shadow Indexing Strategy (Production)

1. Build shadow index: re-embed entire corpus with `gemini-embedding-2` in background
2. Keep production running on legacy model
3. Route 10% traffic to shadow index for A/B testing
4. Recalibrate similarity thresholds (scores will shift — e.g., 0.6 → 0.7)
5. Cut over when metrics are validated

### K3 Migration Checklist

- [ ] Update `build_mrl_index.py`: change MODEL to `models/gemini-embedding-2`
- [ ] Update `forge-embeddings.js`: use `gemini-embedding-2` model name
- [ ] Add task prefixes to all embedding calls
- [ ] Re-embed entire MRL index (~6,296 chunks, ~2 min, ~$2.40)
- [ ] Re-embed Proto_book extraction summaries (~236 chunks, ~$0.10)
- [ ] Recalibrate similarity thresholds in narrative search
- [ ] Update AGENTS.md §300 MRL section with new model name

---

## 8. K3 Integration — Proto_book Narrative Memory

### Indexing Scene Beats
```python
doc = prepare_document(
    content=scene_summary,
    title=f"Ch{chapter_num} Scene {scene_num}"
)
# → "title: Ch3 Scene 2 | text: Ryder confronts Val about the fence..."
```

### Querying Character Knowledge
```python
query = prepare_query(
    "What does Ryder know about Val's corporate past?",
    task="question answering"
)
# → "task: question answering | query: What does Ryder know about..."
```

### Clustering Dialogue Voices
```python
sample = prepare_symmetric(
    '"Fence ain\'t gonna fix itself." He didn\'t look up.',
    task="clustering"
)
# → "task: clustering | query: "Fence ain't gonna fix itself."..."
```

---

## 9. Common Pitfalls

1. **Missing task prefixes = silent failure.** The model still returns vectors, but they're sub-optimal. Always prefix.
2. **Mixing prefix formats.** If docs use `title: X | text: Y`, queries MUST use `task: search result | query: Z`. Never mix.
3. **Cross-model comparison.** Never compare vectors from different embedding models. The latent spaces are incompatible.
4. **Forgetting to normalize after manual truncation.** API-side truncation auto-normalizes. Client-side numpy truncation does not.
5. **Using `task_type` parameter.** This param is for `gemini-embedding-001` only. Embedding-2 ignores it silently.
6. **Batch for throughput.** Use `batchEmbedContents` for 20+ items. Single calls have per-request overhead.
7. **Rate limits.** Free tier: 1,500 RPM. Use `time.sleep(0.3)` between batches.
8. **Threshold drift.** After migration, cosine similarity scores shift. Always recalibrate thresholds.
