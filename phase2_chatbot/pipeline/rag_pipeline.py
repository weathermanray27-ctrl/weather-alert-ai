"""
rag_pipeline.py
---------------
Step 3: Connect Chroma vector DB with an LLM to answer questions.
"""

import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

# --- Config ---
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")

def main():
    # Step 1: Load embeddings and vectorstore
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

    # Step 2: Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Step 3: Connect retriever to LLM using new chain structure
    llm = OpenAI()  # requires OPENAI_API_KEY in environment
    
    prompt = PromptTemplate.from_template(
        """Answer the question based only on the following context:
{context}

Question: {input}

Answer:"""
    )
    
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    qa_chain = create_retrieval_chain(retriever, combine_docs_chain)

    # Step 4: Test query
    query = "What severe weather alerts are active in Arizona?"
    result = qa_chain.invoke({"input": query})
    print("Q:", query)
    print("A:", result["answer"])

if __name__ == "__main__":
    main()
