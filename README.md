# weather-alert-ai

**Repository**: https://github.com/weathermanray27-ctrl/weather-alert-ai

A two-phase project: fetch live NWS weather alerts and power a simple RAG chatbot UI to answer questions about them.

## Phase 1 — Data Pipeline
- Fetch active alerts from the National Weather Service (NWS) API.
- Convert JSON to CSV for downstream processing.

Key scripts:
- `phase1_data_pipeline/scripts/fetch_alerts.py`
- `phase1_data_pipeline/scripts/alerts_to_csv.py`

## Phase 2 — Chatbot (RAG)
Run a Flask app that retrieves relevant alerts from a persisted Chroma vector DB and answers via an LLM.

### LLM Modes
- OpenAI mode: If `OPENAI_API_KEY` is set, uses `langchain-openai` (default `gpt-3.5-turbo`).
- Local mode (Ollama): If `OPENAI_API_KEY` is not set, uses `ChatOllama` (default `mistral`). Ollama must be installed and running, and the model pulled.

### Lazy Initialization
To make the server start fast, embeddings, vector store, and LLM are initialized on the first query rather than at app startup. Expect the first query to take ~30–90 seconds to load models and the DB.

### Quick start
```powershell
# Activate venv
& .\.venv\Scripts\Activate.ps1

# Option A: OpenAI mode
$env:OPENAI_API_KEY="sk-..."

# Start the Flask app (uses OpenAI if key is set, otherwise local Ollama)
python phase2_chatbot\app\chatbot.py
```

### Ollama (local mode)
1. Install Ollama (Windows): open https://ollama.com/download/windows and run the installer. Then open a new PowerShell so PATH refreshes.
2. Start Ollama:
```powershell
ollama serve
```
3. Pull a model:
```powershell
ollama pull mistral
```
4. Optional sanity check:
```powershell
ollama run mistral "Say hello in one sentence."
```

### Dependencies
- langchain, langchain-openai, langchain-community
- langchain-chroma, langchain-huggingface, chromadb
- sentence-transformers, flask, pandas, requests

## Troubleshooting
- OpenAI 401/429: verify your key and billing in the OpenAI dashboard.
- Ollama connection refused: ensure `ollama serve` is running and `mistral` is pulled.
- First query slow: expected due to lazy initialization; subsequent queries are fast.
