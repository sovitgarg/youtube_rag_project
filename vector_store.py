# vector_store.py
import os
from dotenv import load_dotenv
load_dotenv()  # Make sure this loads BEFORE reading from os.getenv

import chromadb
from openai import OpenAI
from sentence_transformers import SentenceTransformer

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Setup persistent Chroma client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="youtube_rag")

embedModel = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text, model=embedModel):
    return model.encode(text).tolist()

def embed_chunks(chunks):
    for chunk in chunks:
        chunk_id = f"{chunk['video_id']}_{int(chunk['start'])}"
        if not _is_chunk_stored(chunk_id):
            embedding = get_embedding(chunk['text'])
            collection.add(
                documents=[chunk['text']],
                metadatas=[chunk],
                ids=[chunk_id]
            )
    return collection, chunks

def _is_chunk_stored(chunk_id):
    try:
        result = collection.get(ids=[chunk_id])
        return len(result['ids']) > 0
    except Exception:
        return False

def search_chunks(query, collection, metadata, top_k=5):
    query_vec = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=top_k
    )

    top_chunks = []
    for text, meta in zip(results['documents'][0], results['metadatas'][0]):
        top_chunks.append({
            "text": text,
            "video_id": meta["video_id"],
            "start": meta["start"],
            "end": meta["end"]
        })

    # ✅ Return only chunks from top matching video
    top_video_id = top_chunks[0]["video_id"] if top_chunks else None
    return [c for c in top_chunks if c["video_id"] == top_video_id]
