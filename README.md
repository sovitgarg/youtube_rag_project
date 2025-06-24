# 🎬 youtube_rag_project

Search your own YouTube channel using natural language.  
This project implements a Retrieval-Augmented Generation (RAG) system to let you query your videos using OpenAI GPT and return precise, timestamped video responses.

It’s like semantic search for your personal video archive.
There is place holder for OpenAI calls, not hooked up with RAG yet.

---

## 🚀 Features

- 🔍 Ask questions about your YouTube videos
- 🧠 GPT-4o powered inference for rich, accurate answers
- 🗂 ChromaDB as persistent vector store (in-memory or disk-backed)
- 🎧 Supports YouTube transcript retrieval (via YouTube API or `youtube-transcript-api`)
- 🎞 Timestamped video playback inside Streamlit
- ✅ Caches transcript chunks and embeddings to avoid redundant processing

---

## 🧰 Tech Stack

- **Streamlit** – frontend UI
- **OpenAI GPT-4o** – inference
- **ChromaDB** – vector database for transcript retrieval
- **YouTube Data API + youtube-transcript-api** – transcript ingestion
- **Python 3.9+**

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/youtube_rag_project.git
cd youtube_rag_project
```

### 2. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up your environment

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your-openai-api-key
YOUTUBE_API_KEY=your-youtube-api-key
YOUTUBE_CHANNEL_ID=your-default-channel-id
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 💡 Example Queries

- "When did I talk about product roadmap?"
- "Which videos discuss deprecating our tools?"
- "Show the video where I said 'coding will be dead in 5 years'"

---

## 📁 Folder Structure

```bash
youtube_rag_project/
├── app.py                   # Main Streamlit app
├── vector_store.py          # Embedding + ChromaDB logic
├── youtube_channel_loader.py # YouTube ingest logic
├── transcript_utils.py      # Transcript formatting & chunking
├── data/
│   └── transcripts/         # Cached transcripts
├── chroma_db/               # ChromaDB persistence
├── requirements.txt
└── .env
```

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙋‍♂️ Author

Made by Sovit Garg – feel free to reach out or fork and modify!
