# ReelMind — YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that lets you ask questions about a YouTube video's spoken content. Paste a video URL, and the system extracts the transcript, indexes it, and answers questions grounded in what was actually said in the video.

## Architecture

- **Frontend:** React (UI only — submits requests, displays results)
- **Backend:** FastAPI (handles all processing and orchestration)
- **Text splitting:** LangChain `RecursiveCharacterTextSplitter`
- **Embeddings:** Hugging Face Sentence Transformers (local, no API key required)
- **Vector store:** FAISS
- **LLM:** Answers generated from retrieved transcript chunks (prompt-augmented generation)

## How It Works

The system has two distinct phases: **Indexing** (prepare a video for search) and **Question Answering** (retrieve relevant info and generate an answer).

### Phase 1 — Submit a video

The user pastes a YouTube URL in the React frontend, which sends it to the backend:

```http
POST /api/videos/process
Content-Type: application/json

{
  "youtube_url": "https://www.youtube.com/watch?v=abc123"
}
```

### Phase 2 — Extract the transcript

The backend extracts the video ID and fetches the available transcript (spoken content only, not video frames).

> **Note:** Transcript availability depends on the video and provider. Some videos have no accessible transcript — this must be handled gracefully in production.

### Phase 3 — Chunk the transcript

Long transcripts are split into smaller, overlapping chunks so the full transcript doesn't need to be sent to the LLM for every question:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(transcript)
```

The overlap (50 chars) helps preserve context for ideas that span a chunk boundary.

### Phase 4 — Generate embeddings

Each chunk is converted into a vector embedding using a local Hugging Face model — no per-request API key needed:

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

`all-MiniLM-L6-v2` produces 384-dimensional embeddings.

### Phase 5 — Store in a vector database

Chunk embeddings and their source text are indexed in **FAISS** for efficient similarity search. Each chunk should also carry metadata for traceability:

```json
{
  "video_id": "abc123",
  "chunk_index": 0,
  "start_time": 0,
  "end_time": 25
}
```

### Phase 6 — Ask a question

When the user asks a question (e.g. *"What is supervised learning?"*), it's embedded using the same model used for the transcript chunks, so it lives in the same vector space.

### Phase 7 — Similarity search

The question vector is compared against stored chunk vectors, and the most relevant chunks are retrieved:

```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)

relevant_chunks = retriever.invoke(
    "What is supervised learning?"
)
```

`k` controls how many chunks are retrieved.

### Phase 8 — Build the prompt and generate an answer

The retrieved chunks are inserted into a prompt template and sent to the LLM, which generates an answer grounded in the retrieved transcript content — this is the bridge between retrieval and generation.

## Tech Stack Summary

| Layer | Technology |
|---|---|
| Frontend | React |
| Backend | FastAPI |
| Transcript extraction | YouTube transcript API |
| Chunking | LangChain `RecursiveCharacterTextSplitter` |
| Embeddings | Hugging Face `sentence-transformers/all-MiniLM-L6-v2` |
| Vector store | FAISS |
| Orchestration | LangChain |
