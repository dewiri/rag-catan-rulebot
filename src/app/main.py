from fastapi import FastAPI
from pydantic import BaseModel
import faiss, json, numpy as np
from openai import OpenAI

app = FastAPI()
client = OpenAI()

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(q: Query):
    # TODO: Query expansion
    # TODO: Embedding & Retrieval
    # TODO: Re-Ranking
    # TODO: Prompt an LLM
    return {"answer": "Noch nicht implementiert"}
