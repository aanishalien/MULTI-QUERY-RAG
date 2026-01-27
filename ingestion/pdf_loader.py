import os
import fitz

def load_pdf(file_path: str):
    doc = fitz.open(file_path)
    paragraphs = []

    for page in doc:
        text = page.get_text("text")
        if text:
            for para in text.split("\n\n"):
                clean_para = para.strip()
                if clean_para:
                    paragraphs.append(clean_para)

    return paragraphs


def load_documents(folder_path: str):
    documents = []

    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)

        if filename.lower().endswith(".pdf"):
            documents.extend(load_pdf(path))

        elif filename.lower().endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                for para in f.read().split("\n\n"):
                    clean_para = para.strip()
                    if clean_para:
                        documents.append(clean_para)

    return documents
