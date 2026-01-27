import faiss
import pickle
import numpy as np
from pathlib import Path
INDEX_PATH = Path("vector_db/faiss.index")
META_PATH = Path("vector_db/faiss_meta.pkl")

def build_faiss_index(vectors: list[list[float]], chunks: list[str]):
    assert len(vectors) == len(chunks), "Number of vectors must match number of chunks."

    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)

    vectors_np = (np.array(vectors).astype('float32'))
    index.add(vectors_np)

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))

    id_to_chunk = {i: chunk for i , chunk in enumerate(chunks)}

    with open(META_PATH, "wb") as f:
        pickle.dump(id_to_chunk, f)

    print(f"FAISS index saved ({index.ntotal}) vectors).")

def load_faiss_index():
    index = faiss.read_index(str(INDEX_PATH))

    with open(META_PATH, "rb") as f:
        id_to_chunk = pickle.load(f)

    return index, id_to_chunk