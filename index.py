import chromadb
from chromadb.utils import embedding_functions

from pdf import load_pdf, chunk_text

def prepare_text(filename):
    text = load_pdf(filename)
    chunks = chunk_text(text)

    client = chromadb.PersistentClient(path="./chroma_db")
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection = client.get_or_create_collection(
        name="personal_collection",
        embedding_function=ef,
    )

    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    collection.add(
        documents=chunks,
        ids=[f"id_{i}" for i in range(len(chunks))],
    )



