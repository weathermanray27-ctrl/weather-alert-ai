"""
ingest.py
----------
Load weather_alerts.csv into LangChain documents.
Each row becomes a Document with metadata for later filtering and retrieval.
"""

import os
import pandas as pd
from langchain_core.documents import Document

# --- Config ---
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "alerts.csv")

def row_to_document(row: pd.Series) -> Document:
    """
    Convert one CSV row into a LangChain Document.
    Text: Concatenate headline + description for semantic retrieval.
    Metadata: Keep key fields for filtering and display.
    """
    headline = str(row.get("headline", "")).strip()
    description = str(row.get("description", "")).strip()
    event = str(row.get("event", "")).strip()
    severity = str(row.get("severity", "")).strip()
    area = str(row.get("areaDesc", "")).strip()
    alert_id = str(row.get("id", "")).strip()
    urgency = str(row.get("urgency", "")).strip()
    certainty = str(row.get("certainty", "")).strip()

    # Core document text used for embeddings and retrieval
    page_content = "\n\n".join(
        [
            f"Event: {event}",
            f"Severity: {severity}",
            f"Area: {area}",
            f"Headline: {headline}",
            f"Description: {description}",
        ]
    )

    # Metadata helps you filter and format answers later
    metadata = {
        "id": alert_id,
        "event": event,
        "severity": severity,
        "areaDesc": area,
        "urgency": urgency,
        "certainty": certainty,
        "headline": headline,
    }

    return Document(page_content=page_content, metadata=metadata)

def load_documents(csv_path: str = CSV_PATH):
    """
    Read CSV into a DataFrame and convert each row to a Document.
    Returns: List[Document]
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    required_cols = ["id", "event", "severity", "areaDesc", "headline", "description"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    docs = [row_to_document(row) for _, row in df.iterrows()]
    return docs

if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")
    # Preview first 1–2 documents
    for d in docs[:2]:
        print("-----")
        print("Metadata:", d.metadata)
        print("Content snippet:", d.page_content[:250], "...")
