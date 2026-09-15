from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

from services.youtube_service import (
    extract_video_id,
    get_transcript,
)

from services.rag_service import (
    create_video_index,
    ask_question,
    RAGServiceError,
)


app = FastAPI(title="YouTube Chatbot API")


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class IndexRequest(BaseModel):
    youtube_url: HttpUrl


class ChatRequest(BaseModel):
    video_id: str
    question: str


# --------------------------------------------------
# Root Route
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "YouTube Chatbot API is running"
    }


# --------------------------------------------------
# Index Video Route
# --------------------------------------------------

@app.post("/api/videos/index")
def index_video(request: IndexRequest):
    try:
        video_id = extract_video_id(
            str(request.youtube_url)
        )

        if not video_id:
            raise ValueError(
                "Could not extract a valid YouTube video ID."
            )

        transcript = get_transcript(video_id)

        if not transcript:
            raise ValueError(
                "Could not retrieve the video transcript."
            )

        result = create_video_index(
            transcript,
            video_id,
        )

        return {
            "message": "Video indexed successfully",
            **result,
        }

    except RAGServiceError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while indexing the video.",
        )


# --------------------------------------------------
# Chat Route
# --------------------------------------------------

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        video_id = request.video_id.strip()
        question = request.question.strip()

        if not video_id:
            raise ValueError("Video ID cannot be empty.")

        if not question:
            raise ValueError("Question cannot be empty.")

        result = ask_question(
            video_id,
            question,
        )

        return result

    except RAGServiceError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the answer.",
        )