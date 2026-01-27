from retrieval.ranker import rank_combined
from retrieval.multi_search import multi_search
from retrieval.query_expander import QueryExpander
from chunking.chunker import chunk_documents

def search(question: str, chunks, top_k: int = 5):
    queries = QueryExpander().expand(question)

    chunk_scores , frequency = multi_search(queries, top_k)

    ranked_chunks = rank_combined(chunk_scores, frequency)

    print("\n--- RETRIEVED CHUNKS ---\n")
    retrieved_chunks = []
    for i, (chunk_idx, score) in enumerate(ranked_chunks[:top_k]):
        chunk_obj = chunks[chunk_idx]
        print(f"Chunk {i+1} (score {score}):\n{chunk_obj}\n")
        retrieved_chunks.append(chunk_obj)


    return retrieved_chunks
