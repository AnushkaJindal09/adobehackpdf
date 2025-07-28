from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def rank_headings_by_relevance(outline, query, model):
    if not outline:
        return []

    headings = [item["text"] for item in outline]
    heading_embeddings = model.encode(headings)
    query_embedding = model.encode([query])[0]

    scores = cosine_similarity([query_embedding], heading_embeddings)[0]

    # Attach scores to headings
    for i, score in enumerate(scores):
        outline[i]["score"] = float(score)

    # Sort by relevance score
    ranked = sorted(outline, key=lambda x: x["score"], reverse=True)

    return ranked
