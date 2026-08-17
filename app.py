import os
import requests
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastapi import HTTPException

from src.rag_pinecone.generation.rag_pipeline import rag_answer


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str

class SuggestionRequest(BaseModel):
    suggestion: str

@app.get("/")
def home():
    return {
        "message": "Foleys Plumbing Compliance Assistant API is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        result = rag_answer(request.question)

        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }

@app.post("/suggestion")
def send_suggestion(request: SuggestionRequest):

    try:

        pushover_token = os.getenv("PUSHOVER_API_TOKEN")
        pushover_user = os.getenv("PUSHOVER_USER_KEY")

        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": pushover_token,
                "user": pushover_user,
                "title": "Foleys AI Assistant Feedback",
                "message": request.suggestion
            },
            timeout=15
        )

        response.raise_for_status()

        return {
            "message": "Suggestion sent successfully"
        }

    except Exception as e:

        print("PUSHOVER ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail="Could not send suggestion"
        )