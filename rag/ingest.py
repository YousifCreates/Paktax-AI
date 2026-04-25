import os
import torch
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Load environment variables
load_dotenv()

# Paths
DOCS_PATH = "data/fbr_docs"
CHROMA_PATH = "chroma_db"

# Detect GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")


def load_documents():
    documents = []
    for filename in os.listdir(DOCS_PATH):
        filepath = os.path.join(DOCS_PATH, filename)
        if filename.endswith(".pdf"):
            print(f"Loading PDF: {filename}")
            loader = PyPDFLoader(filepath)
            documents.extend(loader.load())
        elif filename.endswith(".txt"):
            print(f"Loading TXT: {filename}")
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())
    print(f"Total pages/docs loaded: {len(documents)}")
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", "۔", ".", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    return chunks


def create_vector_store(chunks):
    print("Loading embedding model on GPU...")
    embeddings = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-large",
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True}
    )
    print("Embedding chunks and saving to ChromaDB...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"ChromaDB saved at: {CHROMA_PATH}")
    return vector_store


if __name__ == "__main__":
    print("=== PakTax AI — FBR Document Ingestion ===")
    documents = load_documents()
    if not documents:
        print("No documents found in data/fbr_docs/. Please add FBR documents.")
    else:
        chunks = split_documents(documents)
        create_vector_store(chunks)
        print("Ingestion complete. ChromaDB is ready.")