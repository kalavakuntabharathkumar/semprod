from functools import lru_cache
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@lru_cache(maxsize=1)
def _encoder():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    except Exception:
        return None

def document(product):
    return f"{product.name}. {product.category}. {product.description}. {product.tags}"

def rank(query, products):
    if not products:
        return []
    docs = [document(p) for p in products]
    encoder = _encoder()
    if encoder is not None:
        try:
            vectors = encoder.encode(docs, normalize_embeddings=True)
            qv = encoder.encode([query], normalize_embeddings=True)[0]
            scores = np.asarray(vectors) @ np.asarray(qv)
        except Exception:
            scores = _tfidf_scores(query, docs)
    else:
        scores = _tfidf_scores(query, docs)
    ranked = sorted(zip(products, scores.tolist()), key=lambda pair: pair[1], reverse=True)
    return [{"product": product, "score": round(float(score), 4)} for product, score in ranked]

def _tfidf_scores(query, docs):
    matrix = TfidfVectorizer(stop_words="english", ngram_range=(1,2)).fit_transform(docs + [query])
    return cosine_similarity(matrix[-1], matrix[:-1]).ravel()
