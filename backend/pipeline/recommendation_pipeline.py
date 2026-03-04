from typing import Dict
from src.vector_store import AnimeVectorStore
from src.query_analyzer import QueryAnalyzer
from src.recommender import AnimeRecommender
from src.sentiment_fetcher import SentimentFetcher
from utils.logger import get_logger

logger = get_logger(__name__)


class RecommendationPipeline:
    def __init__(self):
        logger.info("Initializing pipeline...")
        self.vector_store = AnimeVectorStore()
        self.vector_store.get_or_create_collection()
        self.query_analyzer = QueryAnalyzer()
        self.recommender = AnimeRecommender()
        self.sentiment_fetcher = SentimentFetcher()
        logger.info("Pipeline ready.")

    def run(self, user_query: str) -> Dict:
        logger.info(f"Running for: '{user_query}'")

        analysis = self.query_analyzer.analyze(user_query)

        retrieved = self.vector_store.query(
            query_text=analysis["enriched_query"],
            n_results=10,
        )

        if not retrieved:
            return {
                "query": user_query,
                "analysis": analysis,
                "recommendations": [],
                "summary": "No matching anime found. Try rephrasing.",
            }

        llm_result = self.recommender.recommend(
            user_query=user_query,
            analyzed_query=analysis,
            retrieved_anime=retrieved,
        )

        recommendations = llm_result.get("recommendations", [])
        for rec in recommendations:
            title = rec.get("title", "")
            if title:
                sentiment = self.sentiment_fetcher.get_sentiment(title)
                rec["sentiment"] = {
                    "score": sentiment.get("sentiment_score"),
                    "label": sentiment.get("sentiment_label"),
                    "mal_score": sentiment.get("mal_score"),
                    "members": sentiment.get("members"),
                    "popularity_rank": sentiment.get("popularity_rank"),
                    "post_count": sentiment.get("post_count"),
                    "sample_comments": sentiment.get("sample_comments", []),
                    "mal_url": sentiment.get("mal_url", ""),
                }

        return {
            "query": user_query,
            "analysis": {
                "mood": analysis["mood"],
                "themes": analysis["themes"],
                "audience": analysis["audience"],
                "enriched_query": analysis["enriched_query"],
            },
            "recommendations": recommendations,
            "summary": llm_result.get("summary", ""),
        }
