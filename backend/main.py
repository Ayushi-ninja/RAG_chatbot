from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag import ask_question


app = FastAPI()


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5500"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


class ChatRequest(BaseModel):

    question: str


@app.get("/")
def home():

    return {
        "message": "RAG chatbot API is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    result = ask_question(
        request.question
    )

    return result
    