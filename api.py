import os
import logging
import warnings

warnings.filterwarnings("ignore", message=".*AFC.*")
logging.getLogger("google_genai").setLevel(logging.ERROR)

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()
api_key = os.getenv("API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

client = chromadb.PersistentClient(path="./chroma_db")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = client.get_or_create_collection(
    name="personal_collection",
    embedding_function=ef,
)

prompt = "pytanie"
context = collection.query(query_texts=[prompt], n_results=3)


system_prompt = f"""
    pytanie: {prompt}
    kontekst: {context}
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.2
)

answer = llm.invoke(system_prompt)
print()
print(answer.text)