from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from utils.search import answer_question

app = FastAPI()

class Query(BaseModel):
    question: str
    image: Optional[str] = None  # base64 image

@app.post("/api/")
def ask_virtual_ta(query: Query):
    answer, links = answer_question(query.question, query.image)
    return {
        "answer": answer,
        "links": links
    }

