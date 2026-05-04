import os
import torch
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

load_dotenv()

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading embedding model on {device}...")
_embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={"device": device},
    encode_kwargs={"normalize_embeddings": True}
)

print("Connecting to Pinecone...")
_vector_store = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=_embeddings
)

_retriever = _vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 10}
)

print("Retriever ready.")


def get_retriever():
    return _retriever


if __name__ == "__main__":
    print("=== Testing Pinecone Retriever ===")
    test_query = "What is the income tax rate for salaried person in Pakistan?"
    results = _retriever.invoke(test_query)
    print(f"\nQuery: {test_query}")
    print(f"Retrieved {len(results)} chunks:\n")
    for i, doc in enumerate(results):
        print(f"--- Chunk {i+1} ---")
        print(doc.page_content[:300])
        print()