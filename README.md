RAG Chatbot – Local LLM (Qwen 2.5)

A Retrieval-Augmented Generation (RAG) chatbot that answers questions strictly based on uploaded documents, powered by Qwen 2.5 running locally via Ollama.
No external APIs. No data leakage.

🚀 Features

📂 Document-based Question Answering

🔍 Semantic search using embeddings

🧠 Local LLM inference with Qwen 2.5

❌ Zero hallucination (document-only answers)

🔁 Rebuildable vector index

🌐 Simple web UI

🏗️ Architecture
User Query
    ↓
Embedding Model
    ↓
FAISS Vector Store
    ↓
Top-K Relevant Chunks
    ↓
Qwen 2.5 (Local via Ollama)
    ↓
Final Answer

🧩 Tech Stack
Backend

Python

Flask

FAISS

Custom RAG pipeline

Ollama (Qwen 2.5 – Local LLM)

Frontend

React (Vite)

HTML / CSS / JavaScript

Models

LLM: Qwen 2.5 (Local)

Embeddings: Sentence Transformers / Ollama embeddings

📁 Project Structure
rag-chatbot/
│
├── backend/
│   ├── app.py
│   ├── rag.py
│   ├── embeddings.py
│   ├── data/
│   │   └── documents/
│   └── vector_store/
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── requirements.txt
└── README.md

⚙️ Setup & Run
1️⃣ Install Ollama & Qwen 2.5
ollama pull qwen2.5


Verify:

ollama list

2️⃣ Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

3️⃣ Frontend
cd frontend
npm install
npm run dev

🔍 How It Works

Documents are split into small chunks

Each chunk is embedded and stored in FAISS

User submits a query

Top-K relevant chunks are retrieved

Qwen 2.5 generates an answer using only retrieved context

If no relevant context is found, the system responds:

No relevant information found in the document.
