# rag-catan-rulebot
RAG-based rules chatbot for “Settlers of Catan” – answers real-time questions on core rules and expansions.

## Verzeichnisstruktur

- `data/` … Rohdaten und Indizes  
- `src/app/` … Backend (FastAPI)  
- `src/ui/` … Frontend (Streamlit oder React)  
- `docs/` … Projektdokumentation  

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
