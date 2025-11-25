"""
embed.py
---------
Step 2: Split documents into chunks and generate embeddings.
Outputs: Chroma vector database stored in ../data/chroma_db
"""

import os
from ingest import load_documents
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- Config ---
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "alerts.csv")
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")

def main():
    # Step 1: Load documents
    docs = load_documents(CSV_PATH)
    print(f"Loaded {len(docs)} documents")

    # Step 2: Split into chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)
    print(f"Split into {len(split_docs)} chunks")

    # Step 3: Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Step 4: Store in Chroma DB
    vectorstore = Chroma.from_documents(split_docs, embeddings, persist_directory=DB_DIR)
    vectorstore.persist()
    print(f"Persisted vector DB at {DB_DIR}")

if __name__ == "__main__":
    main()
