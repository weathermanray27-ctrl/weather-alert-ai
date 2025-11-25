"""Quick test - query the existing Chroma DB without reloading embeddings"""
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")

print("Loading vector database...")
# Use the same embeddings config as when we created the DB
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

print("Querying for Arizona weather alerts...")
query = "What severe weather alerts are active in Arizona?"
docs = vectorstore.similarity_search(query, k=3)

print(f"\n✅ Retrieved {len(docs)} relevant documents:\n")
for i, doc in enumerate(docs, 1):
    print(f"=== Result {i} ===")
    print(f"Event: {doc.metadata.get('event', 'N/A')}")
    print(f"Severity: {doc.metadata.get('severity', 'N/A')}")
    print(f"Area: {doc.metadata.get('areaDesc', 'N/A')[:100]}")
    print(f"Headline: {doc.metadata.get('headline', 'N/A')[:100]}")
    print()

print("✅ Vector retrieval working! The RAG system can retrieve relevant alerts.")
print("\nTo get natural language answers, run rag_pipeline.py with your OpenAI API key.")
