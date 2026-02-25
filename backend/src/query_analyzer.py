import json
from groq import Groq
from typing import Dict
from config.config import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class QueryAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        logger.info("QueryAnalyzer ready")

    def analyze(self, query: str) -> Dict:
        logger.info(f"Analyzing query: '{query}'")

        prompt = f"""You are an anime expert analyzing a user's search query.

User query: "{query}"

Return a JSON object with:
1. "mood": list of 1-3 mood words (from: happy, sad, melancholic, dark, exciting, romantic, peaceful, thrilling, nostalgic, tense, hopeful, bittersweet)
2. "themes": list of 1-4 themes (from: action, romance, comedy, drama, mystery, fantasy, sci-fi, slice of life, horror, sports, psychological, adventure, supernatural, mecha, historical, isekai, shounen, seinen)
3. "audience": one of: children, teenagers, adults, mature
4. "enriched_query": rewrite the query as a rich 3-5 sentence description for semantic search. Include mood, themes, art style, pacing, and story elements.

Return ONLY valid JSON:
{{
  "mood": ["word1"],
  "themes": ["theme1"],
  "audience": "adults",
  "enriched_query": "detailed paragraph..."
}}"""

        try:
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=400,
            )
            content = response.choices[0].message.content.strip()

            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            result = json.loads(content)

            return {
                "original_query": query,
                "enriched_query": result.get("enriched_query", query),
                "mood": [(m, 0.9) for m in result.get("mood", [])],
                "themes": [(t, 0.9) for t in result.get("themes", [])],
                "audience": [(result.get("audience", "adults"), 0.9)],
            }

        except Exception as e:
            logger.warning(f"Query analysis failed, using original: {e}")
            return {
                "original_query": query,
                "enriched_query": query,
                "mood": [],
                "themes": [],
                "audience": [],
            }
