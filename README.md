# AI-Powered Semantic Product Search & Recommendation Platform

A runnable portfolio implementation of semantic product retrieval and related-item recommendations. The default mode runs locally without paid APIs; Sentence-Transformers and FAISS are optional accelerators. SQLite is used by default for a frictionless start, while `DATABASE_URL` can point to PostgreSQL.

## Features
- FastAPI REST API with product catalog, semantic search, and recommendation endpoints
- Embedding-based retrieval when `sentence-transformers` is installed; deterministic TF-IDF fallback otherwise
- Optional FAISS index; resilient lexical fallback if optional ML packages are unavailable
- Seed catalog of synthetic products, health endpoint, request validation, tests, Dockerfile and GitHub Actions CI
- No real customer/product analytics are included; resume metrics in a project description should be verified against real experiments before being claimed

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate | macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs. Seed products are inserted automatically on first startup.

## API
- `GET /health`
- `GET /products?limit=20`
- `GET /search?q=lightweight+running+shoes&limit=10`
- `GET /recommend/{product_id}?limit=5`
- `GET /explain?q=quiet+headphones` (optional OpenAI API; local fallback if unavailable)

## PostgreSQL
Set `DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/products`. The default is `sqlite:///./products.db`. Set `OPENAI_API_KEY` to enable optional query explanations. Semantic embeddings use Sentence-Transformers when available, with FAISS inner-product retrieval when installed; otherwise the service falls back to TF-IDF.

## Notes
This is a development-ready portfolio baseline, not a production-validated service. For production, add authentication, migrations, monitoring, load testing, data governance, and model/index versioning.
