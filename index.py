import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

from pdf import load_pdf

def clean(text):
    url = r'https?://\S+|www\.\S+'
    mail = r'\S+@\S+'

    text = re.sub(' +', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(url, '', text)
    text = re.sub(mail, '', text)

    return text

def prepare_text(filename):
    text = load_pdf(filename)
    text = clean(text)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,    
        chunk_overlap=100,  
        length_function=len,
        is_separator_regex=False
    )

    chunks = text_splitter.split_text(text)

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

prepare_text("file.pdf")