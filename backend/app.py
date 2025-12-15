import os
import shutil
from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_pipeline import RAG

app = Flask(__name__)
CORS(app)

rag = RAG()

UPLOAD_FOLDER = "data/documents"


@app.post("/upload")
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # 🔥 CLEAR OLD DOCUMENTS (IMPORTANT)
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    # Rebuild index ONLY for this PDF
    rag.rebuild_index()

    return jsonify({"message": "File uploaded and index updated"})


@app.post("/ask")
def ask():
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"answer": "No question provided"}), 400

    answer = rag.query(query)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
