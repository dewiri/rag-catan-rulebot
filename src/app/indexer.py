import os
import json
import faiss
import numpy as np
from openai import OpenAI

def generate_embeddings(chunks, model: str = "text-embedding-ada-002") -> np.ndarray:
    """
    Call OpenAI to generate embeddings for each chunk.
    Returns a 2D numpy array of shape (num_chunks, embedding_dim).
    """
    client = OpenAI()
    embeddings = []
    for chunk in chunks:
        resp = client.embeddings.create(
            input=chunk["text"],
            model=model
        )
        vec = np.array(resp["data"][0]["embedding"], dtype="float32")
        embeddings.append(vec)
    return np.vstack(embeddings)

def build_faiss_index(embeddings: np.ndarray, index_path: str = "data/index/faiss.index"):
    """
    Build an HNSWFlat FAISS index from embeddings and save to disk.
    """
    dim = embeddings.shape[1]
    index = faiss.IndexHNSWFlat(dim, 32)  # 32 = number of neighbors in HNSW graph
    index.add(embeddings)
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)
    print(f"Index saved to {index_path}")

def save_metadata(chunks, metadata_path: str = "data/index/metadata.json"):
    """
    Save the list of chunk metadata (including text) to disk as JSON.
    """
    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"Metadata saved to {metadata_path}")

def main():
    # 1) Load preprocessed chunks
    with open("data/index/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # 2) Generate embeddings
    embeddings = generate_embeddings(chunks)

    # 3) Build and save FAISS index
    build_faiss_index(embeddings)

    # 4) Save chunk metadata
    save_metadata(chunks)

if __name__ == "__main__":
    main()
