import torch
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Paths
CHROMA_PATH = "chroma_db"

# Detect GPU
device = "cuda" if torch.cuda.is_available() else "cpu"


def get_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-large",
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True}
    )

    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10}
    )

    return retriever


if __name__ == "__main__":
    print("=== Testing Retriever ===")
    retriever = get_retriever()
    test_query = "What is the income tax rate for salaried person in Pakistan?"
    results = retriever.invoke(test_query)
    print(f"\nQuery: {test_query}")
    print(f"Retrieved {len(results)} chunks:\n")
    for i, doc in enumerate(results):
        print(f"--- Chunk {i+1} ---")
        print(doc.page_content[:300])
        print()