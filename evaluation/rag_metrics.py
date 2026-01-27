import numpy as np
from embeddings.embedder import embed_query
from vector_db.faiss_store import load_faiss_index

def search(query: str, top_k=5):
    index, chunks = load_faiss_index()

    query_vector = embed_query(query)
    query_vector = np.array(query_vector).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []
    for i in indices[0]:
        if 0 <= i < len(chunks):
            results.append(chunks[i])
    return results