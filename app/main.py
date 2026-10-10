from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import Product
from .seed import seed_products
from .search import rank
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with next(get_db()) as db:
        seed_products(db)
    yield

app = FastAPI(title="Semantic Product Search API", version="1.0.0", lifespan=lifespan)

def serialize(p: Product):
    return {"id": p.id, "name": p.name, "category": p.category, "description": p.description, "price": p.price, "tags": p.tags}

@app.get("/health")
def health():
    return {"status": "ok", "service": "semantic-product-search"}

@app.get("/products")
def products(limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    return [serialize(p) for p in db.query(Product).order_by(Product.id).limit(limit).all()]

@app.get("/search")
def search(q: str = Query(..., min_length=2, max_length=250), limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    all_products = db.query(Product).all()
    ranked = rank(q, all_products)[:limit]
    return {"query": q, "count": len(ranked), "results": [{**serialize(row["product"]), "score": row["score"]} for row in ranked]}

@app.get("/recommend/{product_id}")
def recommend(product_id: int, limit: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)):
    source = db.get(Product, product_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Product not found")
    candidates = db.query(Product).filter(Product.id != product_id).all()
    ranked = rank(f"{source.name} {source.category} {source.description} {source.tags}", candidates)[:limit]
    return {"product": serialize(source), "recommendations": [{**serialize(r["product"]), "score": r["score"]} for r in ranked]}

@app.get("/explain")
def explain(q: str = Query(..., min_length=2, max_length=250)):
    """Return a short search explanation; uses OpenAI when configured, otherwise a local fallback."""
    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                input=f"Explain in one concise sentence what kinds of products this ecommerce search query seeks: {q!r}. Do not invent specific inventory."
            )
            return {"query": q, "explanation": response.output_text, "mode": "llm"}
        except Exception:
            pass
    return {"query": q, "explanation": f"Searching product names, categories, descriptions, and tags related to: {q}.", "mode": "fallback"}
