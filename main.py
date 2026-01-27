from ingestion.pdf_loader import load_pdf
from chunking.chunker import chunk_documents
from embeddings.embedder import embed_chunks
from vector_db.faiss_store import build_faiss_index
from generation.llm_generate import generate_answer
from retrieval.search import search

docs = load_pdf("data/docs/FULLTEXT01.pdf")
chunks = chunk_documents(docs)

vectors = embed_chunks(chunks)
build_faiss_index(vectors, chunks)

question = "what is whitespace tokenization and character tokenization ?"

ranked_chunks = search(question, chunks)

answer = generate_answer(question, ranked_chunks)

print("\n Anwser:\n")
print(answer)

