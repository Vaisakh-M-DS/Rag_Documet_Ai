def clean_text(text):
    return " ".join(text.split())

def chunk_text(text, size=800):
    words = text.split()
    chunks = [" ".join(words[i:i+size]) for i in range(0, len(words), size)]
    return chunks
