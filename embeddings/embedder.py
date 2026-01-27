from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: list[str]):
    vectors = model.encode(chunks, show_progress_bar=True)
    return vectors

def embed_query(query: str):
    vector = model.encode([query])
    return vector.tolist()

