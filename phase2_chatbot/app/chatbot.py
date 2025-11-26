"""
chatbot.py
-----------
Flask app that exposes a simple chat UI for querying weather alerts via RAG.
"""

import os
from flask import Flask, request, render_template
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- Config paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "data", "chroma_db")

# --- Lazy init of embeddings/vector store to speed app startup ---
embeddings = None
vectorstore = None
retriever = None

def get_retriever():
    global embeddings, vectorstore, retriever
    if retriever is None:
        # Import heavy dependencies lazily to improve app startup time
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_chroma import Chroma
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever

# Choose LLM: OpenAI if OPENAI_API_KEY is set, otherwise fallback to local Ollama
LLM_INIT_ERROR = None
openai_key = os.getenv("OPENAI_API_KEY")
# Defer LLM import/initialization until first query to avoid heavy imports at startup
llm_mode = "openai" if openai_key else "ollama"
llm = None

# Create RAG prompt template
template = """Answer the question based only on the following context:

{context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

# Format retrieved docs
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Create RAG chain
qa_chain = None

@app.route("/", methods=["GET", "POST"])
def chat():
    answer = None
    query = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if LLM_INIT_ERROR:
            answer = LLM_INIT_ERROR
        elif query:
            try:
                # Build chain on first use (ensures retriever is initialized lazily)
                global qa_chain
                if qa_chain is None:
                    retr = get_retriever()
                    # Initialize LLM lazily based on mode
                    global llm
                    if llm is None:
                        try:
                            if llm_mode == "openai":
                                from langchain_openai import ChatOpenAI
                                llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
                            else:
                                from langchain_community.chat_models import ChatOllama
                                llm = ChatOllama(model="mistral", temperature=0)
                        except Exception as e:
                            answer = f"LLM initialization failed: {str(e)}"
                            return render_template("index.html", query=query, answer=answer)
                    qa_chain = (
                        {"context": retr | format_docs, "question": RunnablePassthrough()}
                        | prompt
                        | llm
                        | StrOutputParser()
                    )
                answer = qa_chain.invoke(query)
            except Exception as e:
                answer = f"Error: {str(e)}"

    return render_template("index.html", query=query, answer=answer)

@app.route("/health", methods=["GET"]) 
def health():
    # Basic health check endpoint: returns 200 if the app is responsive
    return {"status": "ok"}, 200

if __name__ == "__main__":
    # For local dev only
    app.run(host="127.0.0.1", port=5000, debug=True)

