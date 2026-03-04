import json
from groq import Groq
from typing import List, Dict
from config.config import get_settings
from src.prompt_template import build_recommendation_prompt
from utils.logger import get_logger
from utils.exceptions import RecommendationError

logger = get_logger(__name__)
settings = get_settings()


class AnimeRecommender:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    def recommend(self, user_query: str, analyzed_query: Dict, retrieved_anime: List[Dict]) -> Dict:
        prompt = build_recommendation_prompt(user_query, analyzed_query, retrieved_anime)
        logger.info("Sending to Groq...")

        try:
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500,
            )
        except Exception as e:
            raise RecommendationError(f"Groq API error: {e}")

        content = response.choices[0].message.content.strip()

        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        try:
            result = json.loads(content)
            logger.info(f"Got {len(result.get('recommendations', []))} recommendations")
            return result
        except json.JSONDecodeError:
            raise RecommendationError(f"Invalid JSON from LLM: {content[:200]}")
