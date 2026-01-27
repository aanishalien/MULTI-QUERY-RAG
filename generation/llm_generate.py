import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Use Claude 3.5 Haiku - fast and affordable for RAG
LLM_MODEL = "claude-3-5-haiku-20241022"

def generate_answer(question: str, retrieved_chunks: list[str]):
    """
    If the answer is not contained in the context, say "I don't know based on the provided documents."

    """
    
    # Combine all chunks as context with numbering
    context = "\n\n".join([f"[Chunk {i+1}]\n{chunk}" for i, chunk in enumerate(retrieved_chunks)])
    
    prompt = f"""
You are a factual AI assistant.

Rules:
- Answer ONLY using the provided context
- If the answer is not present, say: "I don't know based on the provided documents"
- Cite chunks like [Chunk 1], [Chunk 2]

Context:
{context}

Question:
{question}
"""

    
    # THIS IS THE CORRECT API CALL - Messages API
    response = client.messages.create(
        model=LLM_MODEL,
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract text from response
    return response.content[0].text
