from embeddings import DocIndexer
import ollama

SUMMARY_QUESTIONS = [
    "tell about pdf",
    "tell about document",
    "explain this document",
    "summarize the pdf",
    "what is this pdf about",
    "overview of document",
    "tell about uploaded pdf"
]


def summary_prompt(context):
    return f"""
You are an intelligent assistant.

TASK:
- Summarize the document using ONLY the context.
- Do NOT copy text directly.
- Explain in SIMPLE, HUMAN language.
- Use short bullet points.
- Max 6 bullets.
- No unnecessary technical jargon.

CONTEXT:
{context}

SUMMARY:
"""


def strict_prompt(context, question):
    return f"""
You are a strict document-based assistant.

RULES:
- Answer ONLY using the context.
- If answer is NOT clearly present, reply EXACTLY:
  "No relevant information found in the document."
- Use bullet points only.
- One idea per bullet.
- Max 6 bullets.
- No explanations outside context.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


class RAG:
    def __init__(self):
        self.indexer = DocIndexer()
        self.indexer.load()

    def rebuild_index(self):
        self.indexer.build_index("data/documents")
        self.indexer.save()

    def query(self, question):
        docs = self.indexer.search(question, k=5)

        if not docs:
            return "No relevant information found in the document."

        context = "\n\n".join(docs)
        q = question.lower().strip()

        is_summary = any(x in q for x in SUMMARY_QUESTIONS)

        if is_summary:
            prompt = summary_prompt(context)
        else:
            prompt = strict_prompt(context, question)

        response = ollama.generate(
            model="qwen2.5",
            prompt=prompt,
            options={"temperature": 0.2}
        )

        return response["response"].strip()
