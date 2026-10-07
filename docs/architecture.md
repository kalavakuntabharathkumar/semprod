# Architecture

```text
Client -> FastAPI routes -> SQLAlchemy -> SQLite/PostgreSQL
                       -> ranking service -> Sentence-Transformers (optional)
                                         -> TF-IDF fallback
```

The first implementation ranks the full catalog for simplicity. For a 120K+ catalog, batch embeddings offline, persist vectors, use FAISS/HNSW for candidate retrieval, and apply a learned or rule-based reranker to a small candidate set. Track NDCG@K, Recall@K, zero-result rate, click-through rate, p50/p95 latency, and index freshness on a representative evaluation set before claiming impact.
