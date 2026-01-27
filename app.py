from fastapi import FastAPI,UploadFile,File
from typing import List
from ingestion.pdf_loader import load_pdf
from chunking.chunker import chunk_documents
from embeddings.embedder import embed_chunks
from vector_db.faiss_store import build_faiss_index
from pydantic import BaseModel
from retrieval.search import search
from generation.llm_generate import generate_answer
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALL_CHUNKS = []

@app.post("/uploads")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    global ALL_CHUNKS

    all_paragraphs = []
    documents_info = []   # 🔥 what frontend needs

    for file in files:
        temp_path = f"temp_{file.filename}"

        with open(temp_path, "wb") as f:
            f.write(await file.read())

        paragraphs = load_pdf(temp_path)
        os.remove(temp_path)

        # Count chunks per file
        file_chunks = chunk_documents(paragraphs)

        documents_info.append({
            "id": file.filename,
            "name": file.filename,
            "chunks": len(file_chunks)
        })

        all_paragraphs.extend(paragraphs)

    # Global chunks for search
    ALL_CHUNKS = chunk_documents(all_paragraphs)

    vectors = embed_chunks(ALL_CHUNKS)
    build_faiss_index(vectors, ALL_CHUNKS)

    return {
        "documents": documents_info,
        "total_chunks": len(ALL_CHUNKS)
    }


class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(request: ChatRequest):
    if not ALL_CHUNKS:
        return {"error": "No documents have been uploaded yet."}
    
    retrieved_chunks = search(request.question, ALL_CHUNKS)

    answer = generate_answer(request.question, retrieved_chunks)

    return {
        "question": request.question,
        "answer": answer
    }