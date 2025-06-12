# YouTube RAG with Streamlit, Whisper, and OpenAI

# 🔧 Folder Structure:
# youtube-rag/
# ├── app.py                   ← Streamlit UI
# ├── transcript_utils.py      ← Transcription & chunking
# ├── vector_store.py          ← Embedding & retrieval
# ├── youtube_channel_loader.py← YouTube transcript importer + timestamp links
# ├── data/
# │   └── transcripts/         ← Timestamped transcripts
# ├── .env                     ← API keys
# └── requirements.txt

# app.py
import streamlit as st
import os
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from transcript_utils import get_all_transcript_chunks
from vector_store import embed_chunks, search_chunks
from youtube_channel_loader import get_youtube_url_with_start_time, download_transcripts_from_channel

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🎬 YouTube RAG with GPT-4o")

import streamlit as st
import os

# Show input box to override default if needed
channel_id_input = st.text_input("Enter YouTube Channel ID", value="")

# Use user input if provided, else fallback to default
channel_id = channel_id_input.strip() if channel_id_input.strip() else os.getenv("YOUTUBE_CHANNEL_ID")


if st.button("Update transcripts from YouTube channel"):
    with st.spinner("Fetching transcripts from YouTube..."):
        download_transcripts_from_channel(channel_id)
        st.success("Transcript update complete!")

query = st.text_input("Ask your question about your video library")

if query:
    chunks = get_all_transcript_chunks()
    index, metadata = embed_chunks(chunks)

    top_chunks = search_chunks(query, index, metadata)
    context = "\n".join([c['text'] for c in top_chunks])

    prompt = f"""
    You are a helpful assistant. Use the following transcript excerpts from one or more YouTube videos to answer the user's question.
    Only use the information from the transcript. If the answer is not explicitly present or inferable, say: "The transcripts don't contain a clear answer."
    Be context-aware and accurate as much as possible, but if you think that an answer is largely correct then present that as well.

    Transcript Segments:
    {context}

    Question:
    {query}
    """

    print("\n====== PROMPT SENT TO GPT-4o ======\n")
    print(prompt)
    print("\n===================================\n")

    with st.spinner("Calling GPT-4o..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content

    st.subheader("Answer")
    st.markdown(answer)

    st.subheader("Relevant Segments")
    for chunk in top_chunks:
        start = int(chunk['start'])
        video_id = chunk['video_id']
        video_url = f"https://www.youtube.com/embed/{video_id}?start={start}&mute=0"
        st.markdown(
            f"""
            <iframe width="560" height="315"
            src="https://www.youtube.com/embed/{video_id}?start={start}"
            frameborder="0"
            allow="autoplay; encrypted-media"
            allowfullscreen></iframe>
            """,
            unsafe_allow_html=True
        )
        st.caption(f"{chunk['text']}\n(Start: {chunk['start']}s)")

