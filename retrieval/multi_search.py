from embeddings.embedder import embed_query
from vector_db.faiss_store import load_faiss_index
import numpy as np
from collections import Counter

def multi_search(queries: list[str], top_k=3):
    index, id_to_chunk = load_faiss_index()

    chunk_scores = {}
    frequency = Counter()

    for query in queries:
        query_vec = embed_query(query)
        query_vec = np.array(query_vec).astype("float32")

        distances, indices = index.search(query_vec, top_k)

        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue

            score = -dist
            frequency[idx] += 1
            chunk_scores[idx] = max(chunk_scores.get(idx, 0), score)
        
    return chunk_scores, frequency