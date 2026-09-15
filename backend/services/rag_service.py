import logging
import os
from typing import Dict, Any

from dotenv import load_dotenv

from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEmbeddings,
    HuggingFaceEndpoint,
)


from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Prompt Template
# --------------------------------------------------

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful YouTube video assistant.

Answer the question using only the provided transcript context.

If the answer is not present in the context, say:
"I could not find that information in the video transcript."

Context:
{context}

Question:
{question}
"""
)


# Stores retrievers for indexed videos
video_retrievers: Dict[str, Any] = {}


# --------------------------------------------------
# Custom Exceptions
# --------------------------------------------------

class RAGServiceError(Exception):
    """Base exception for RAG service errors."""


class ModelInitializationError(RAGServiceError):
    """Raised when embeddings or LLM initialization fails."""


class VideoIndexingError(RAGServiceError):
    """Raised when video indexing fails."""


class QuestionAnsweringError(RAGServiceError):
    """Raised when question answering fails."""


# --------------------------------------------------
# Model Initialization
# --------------------------------------------------

def get_models():
    """
    Initialize Hugging Face embeddings and chat model.
    """

    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        logger.error("HF_TOKEN is missing from the environment.")

        raise ModelInitializationError(
            "Hugging Face token is missing. "
            "Add HF_TOKEN to backend/.env and restart the server."
        )

    try:
        logger.info("Initializing Hugging Face embeddings.")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        logger.info("Initializing Hugging Face chat model.")

        llm_endpoint = HuggingFaceEndpoint(
            repo_id="HuggingFaceH4/zephyr-7b-beta",
            task="conversational",
            max_new_tokens=512,
            temperature=0.1,
            huggingfacehub_api_token=hf_token,
        )

        llm = ChatHuggingFace(llm=llm_endpoint)

        return embeddings, llm

    except Exception as error:
        logger.exception(
            "Failed to initialize Hugging Face models: %s",
            error,
        )

        raise ModelInitializationError(
            "Unable to initialize Hugging Face models. "
            "Check your HF_TOKEN and model configuration."
        ) from error


# --------------------------------------------------
# Create Video Index
# --------------------------------------------------

def create_video_index(transcript: str, video_id: str):
    """
    Split the transcript, create embeddings, and build a FAISS index.
    """

    if not video_id or not video_id.strip():
        raise VideoIndexingError("Video ID cannot be empty.")

    if not transcript or not transcript.strip():
        raise VideoIndexingError(
            "Transcript cannot be empty. "
            "Make sure the video has an available transcript."
        )

    video_id = video_id.strip()

    try:
        logger.info("Creating index for video: %s", video_id)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
        )

        documents = splitter.create_documents([transcript])

        if not documents:
            raise VideoIndexingError(
                "No document chunks were created from the transcript."
            )

        embeddings, _ = get_models()

        vectorstore = FAISS.from_documents(
            documents,
            embeddings,
        )

        video_retrievers[video_id] = vectorstore.as_retriever(
            search_kwargs={"k": 4}
        )

        logger.info(
            "Successfully indexed video %s with %s chunks.",
            video_id,
            len(documents),
        )

        return {
            "success": True,
            "video_id": video_id,
            "chunks": len(documents),
        }

    except RAGServiceError:
        raise

    except Exception as error:
        logger.exception(
            "Failed to create index for video %s: %s",
            video_id,
            error,
        )

        raise VideoIndexingError(
            "An unexpected error occurred while indexing the video."
        ) from error


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

def ask_question(video_id: str, question: str):
    """
    Retrieve relevant transcript chunks and generate an answer.
    """

    if not video_id or not video_id.strip():
        raise QuestionAnsweringError("Video ID cannot be empty.")

    if not question or not question.strip():
        raise QuestionAnsweringError("Question cannot be empty.")

    video_id = video_id.strip()
    question = question.strip()

    retriever = video_retrievers.get(video_id)

    if retriever is None:
        raise QuestionAnsweringError(
            "Video index not found. Please index the video before asking questions."
        )

    try:
        logger.info(
            "Processing question for video %s: %s",
            video_id,
            question,
        )

        documents = retriever.invoke(question)

        if not documents:
            return {
                "success": True,
                "answer": (
                    "I could not find relevant information "
                    "in the video transcript."
                ),
                "sources": [],
            }

        context = "\n\n".join(
            document.page_content
            for document in documents
            if document.page_content
        )

        if not context.strip():
            return {
                "success": True,
                "answer": (
                    "I could not find relevant information "
                    "in the video transcript."
                ),
                "sources": [],
            }

        _, llm = get_models()

        chain = prompt | llm | StrOutputParser()

        answer = chain.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        if not answer or not answer.strip():
            raise QuestionAnsweringError(
                "The language model returned an empty response."
            )

        logger.info("Successfully generated answer for video %s.", video_id)

        return {
            "success": True,
            "answer": answer.strip(),
            "sources": [
                document.page_content
                for document in documents
                if document.page_content
            ],
        }

    except RAGServiceError:
        raise

    except Exception as error:
        logger.exception(
            "Failed to answer question for video %s: %s",
            video_id,
            error,
        )

        raise QuestionAnsweringError(
            "An unexpected error occurred while generating the answer."
        ) from error


# --------------------------------------------------
# Optional Utility Function
# --------------------------------------------------

def delete_video_index(video_id: str):
    """
    Remove a video index from memory.
    """

    if not video_id or not video_id.strip():
        raise ValueError("Video ID cannot be empty.")

    video_id = video_id.strip()

    if video_id not in video_retrievers:
        return {
            "success": False,
            "message": "Video index was not found.",
        }

    del video_retrievers[video_id]

    logger.info("Deleted index for video %s.", video_id)

    return {
        "success": True,
        "message": "Video index deleted successfully.",
    }