from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from .storage import init_db, save_review, list_reviews, get_review
from .llm import analyze
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="LLM Code Review System", version="0.1.0", lifespan=lifespan)

class ReviewRequest(BaseModel):
    language: str = Field(min_length=1, max_length=30)
    code: str = Field(min_length=1, max_length=20000)

@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/reviews")
async def create_review(data: ReviewRequest):
    result, mode = await analyze(data.code, data.language)
    return save_review(data.language, data.code, result, mode)

@app.get("/api/reviews")
def reviews():
    return list_reviews()

@app.get("/api/reviews/{review_id}")
def review(review_id: str):
    item = get_review(review_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return item
