import os
import faiss
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from utils import clean_text, chunk_text
import numpy as np
import pickle

class DocIndexer:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.text_chunks = []

    def extract_text(self, path):
        text = ""
        try:
            pdf = PdfReader(path)
            for page in pdf.pages:
                text += page.extract_text() or ""
        except:
            print(f"[WARNING] Cannot read PDF: {path}")
        return clean_text(text)

    def build_index(self, folder):

        self.text_chunks = []
        documents = os.listdir(folder)

        for doc in documents:
            if not doc.lower().endswith(".pdf"):
                continue

            full_path = os.path.join(folder, doc)
            print("[index] reading", doc)

            raw = self.extract_text(full_path)
            chunks = chunk_text(raw)
            self.text_chunks.extend(chunks)

        embeddings = self.model.encode(self.text_chunks, convert_to_numpy=True)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def search(self, query, k=5):
        query_emb = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_emb, k)

        return [self.text_chunks[i] for i in I[0]]

    def save(self):
        faiss.write_index(self.index, "data/faiss.index")
        with open("data/text.pkl", "wb") as f:
            pickle.dump(self.text_chunks, f)

    def load(self):
        try:
            self.index = faiss.read_index("data/faiss.index")
            with open("data/text.pkl", "rb") as f:
                self.text_chunks = pickle.load(f)
        except:
            print("[INFO] No existing index found.")
