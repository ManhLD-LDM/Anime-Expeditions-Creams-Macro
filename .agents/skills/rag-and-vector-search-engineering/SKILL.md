---
name: rag-and-vector-search-engineering
description: Standards and pipelines for Advanced Retrieval-Augmented Generation (RAG), Hybrid Search, Semantic Chunking, Vector Databases, and Context Budget Optimization.
---

# Advanced RAG & Vector Search Engineering

This skill defines the architectural pipeline for building production-grade RAG systems that eliminate hallucinations and maximize retrieval precision.

---

## 1. Production Advanced RAG Pipeline

```
[User Query]
     │
     ▼
[Query Transformation (HyDE / Multi-Query Expansion)]
     │
     ├──────────────────────────┬──────────────────────────┐
     ▼                          ▼                          ▼
[Dense Vector Search]     [Sparse BM25 Search]     [Metadata Filter]
 (Cosine / HNSW Index)    (Exact Keyword Matches)   (tenant_id, date)
     │                          │                          │
     └──────────────────────────┼──────────────────────────┘
                                │
                                ▼
               [Reciprocal Rank Fusion (RRF)]
                                │
                                ▼
               [Cross-Encoder Reranker (Top-K)]
                                │
                                ▼
               [Context Assembly & Prompt Budget]
                                │
                                ▼
                 [LLM Grounded Generation]
```

---

## 2. Chunking & Ingestion Strategies

1. **Markdown & AST-Aware Chunking (Best for Code/Docs)**:
   - Chunk by structural headers (`#`, `##`, `###`) to preserve conceptual cohesion.
   - Attach parent header metadata to each chunk (`{"section": "Authentication > JWT"}`).
2. **Recursive Character Chunking**:
   - Chunk size: `500 - 1000` tokens.
   - Overlap: `10 - 20%` (e.g. 100 tokens) to maintain sentence boundaries.
3. **Parent-Child Document Strategy**:
   - Index small child chunks (100-200 tokens) for sharp semantic vector matching.
   - Retrieve and feed the larger parent chunk (1000 tokens) to the LLM for rich context.

---

## 3. Hybrid Search & Reciprocal Rank Fusion (RRF)

Combine sparse (keyword) and dense (semantic vector) scores to avoid vocabulary mismatch:

$$\text{RRF Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where $k \approx 60$ and $r_m(d)$ is the document rank in search system $m$.

---

## 4. Query Transformation Techniques

1. **HyDE (Hypothetical Document Embeddings)**:
   - Generate a hypothetical ideal answer with a fast model first.
   - Embed the hypothetical answer and search for real documents matching its semantic signature.
2. **Sub-Query Decomposition**:
   - Break multi-part user questions ("Compare Postgres vs MongoDB pricing and scale") into 2 independent sub-queries.
3. **Contextual Query Rewriting**:
   - Resolve conversational pronouns ("How do I install it?") into fully qualified queries ("How do I install PostgreSQL on Ubuntu?").

---

## 5. Reranking & Lost-in-the-Middle Mitigation

- **Cross-Encoder Reranking**: Re-score the top 20 candidate chunks with a specialized reranker (Cohere Rerank / BGE-Reranker-v2), selecting only the top 3-5 highest scoring chunks.
- **Context Positioning**: Place the most critical reference documents at the **very beginning** or **very end** of the context prompt, as LLMs suffer attention degradation on information buried in the middle of large prompts.
