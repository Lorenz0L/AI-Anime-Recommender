from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from typing import Optional
from pipeline.recommendation_pipeline import RecommendationPipeline
from utils.logger import get_logger

logger = get_logger(__name__)

_pipeline: Optional[RecommendationPipeline] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _pipeline
    logger.info("Starting up...")
    _pipeline = RecommendationPipeline()
    logger.info("Ready.")
    yield
    logger.info("Shutting down.")


app = FastAPI(title="AniMind API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=500)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/recommend")
async def recommend(request: RecommendRequest):
    if _pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not ready")
    try:
        return _pipeline.run(request.query)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sentiment/{anime_title}")
async def get_sentiment(anime_title: str):
    if _pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not ready")
    try:
        return _pipeline.sentiment_fetcher.get_sentiment(anime_title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"app": "AniMind", "docs": "/docs"}
