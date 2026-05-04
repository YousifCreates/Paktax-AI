import os
import torch
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

load_dotenv()

DOCS_PATH = "data/fbr_docs"
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
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
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    return chunks


def create_vector_store(chunks):
    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-large",
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True}
    )

    print("Connecting to Pinecone...")
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    # Create index if it doesn't exist
    existing_indexes = [i.name for i in pc.list_indexes()]
    if INDEX_NAME not in existing_indexes:
        print(f"Creating Pinecone index: {INDEX_NAME}")
        pc.create_index(
            name=INDEX_NAME,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    else:
        print(f"Index '{INDEX_NAME}' already exists. Skipping creation.")

    print("Embedding chunks and uploading to Pinecone...")
    vector_store = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=INDEX_NAME
    )

    print("Pinecone ingestion complete.")
    return vector_store


if __name__ == "__main__":
    print("=== PakTax AI — Pinecone Document Ingestion ===")
    documents = load_documents()
    if not documents:
        print("No documents found in data/fbr_docs/. Please add FBR documents.")
    else:
        chunks = split_documents(documents)
        create_vector_store(chunks)
        print("Ingestion complete. Pinecone is ready.")