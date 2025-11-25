"""Simple test to verify RAG pipeline components"""
import os
print("Step 1: Importing libraries...")
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")

print("Step 2: Loading embeddings model...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("✓ Embeddings loaded")

print("Step 3: Loading vector database...")
vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
print("✓ Vector database loaded")

print("Step 4: Testing retrieval...")
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
docs = retriever.invoke("Arizona weather alerts")
print(f"✓ Retrieved {len(docs)} documents")

for i, doc in enumerate(docs, 1):
    print(f"\n--- Document {i} ---")
    print(f"Event: {doc.metadata.get('event', 'N/A')}")
    print(f"Area: {doc.metadata.get('areaDesc', 'N/A')}")
    print(f"Severity: {doc.metadata.get('severity', 'N/A')}")
    print(f"Content preview: {doc.page_content[:200]}...")

print("\n✅ RAG components working! Ready to add LLM.")
