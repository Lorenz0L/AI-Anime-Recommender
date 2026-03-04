import httpx
import time
from typing import Dict
from utils.logger import get_logger

logger = get_logger(__name__)
JIKAN_BASE = "https://api.jikan.moe/v4"


class SentimentFetcher:
    def __init__(self):
        self._cache: Dict[str, Dict] = {}
        self._timestamps: Dict[str, float] = {}
        self.ttl = 3600
        logger.info("SentimentFetcher ready")

    def get_sentiment(self, title: str) -> Dict:
        if self._cached(title):
            return {**self._cache[title], "from_cache": True}
        try:
            result = self._fetch(title)
            self._cache[title] = result
            self._timestamps[title] = time.time()
            return {**result, "from_cache": False}
        except Exception as e:
            logger.warning(f"MAL fetch failed for '{title}': {e}")
            return self._empty(title)

    def _fetch(self, title: str) -> Dict:
        time.sleep(0.4)
        with httpx.Client(timeout=10.0) as client:
            r = client.get(f"{JIKAN_BASE}/anime", params={"q": title, "limit": 1, "sfw": False})
            if r.status_code == 429:
                time.sleep(2)
                r = client.get(f"{JIKAN_BASE}/anime", params={"q": title, "limit": 1, "sfw": False})
            r.raise_for_status()
            data = r.json()

        results = data.get("data", [])
        if not results:
            return self._empty(title)

        a = results[0]
        mal_score = a.get("score")
        members = a.get("members", 0)
        scored_by = a.get("scored_by", 0)
        popularity = a.get("popularity")

        sentiment_score = round(mal_score / 10.0, 3) if mal_score else None
        label = (
            "unknown" if sentiment_score is None
            else "positive" if sentiment_score >= 0.75
            else "mixed" if sentiment_score >= 0.60
            else "negative"
        )

        comments = []
        if mal_score:
            comments.append(f"Rated {mal_score}/10 by {scored_by:,} MAL users")
        if members:
            comments.append(f"{members:,} people have this in their list")
        if popularity:
            comments.append(f"#{popularity} most popular on MyAnimeList")

        return {
            "title": a.get("title", title),
            "sentiment_score": sentiment_score,
            "sentiment_label": label,
            "mal_score": mal_score,
            "members": members,
            "scored_by": scored_by,
            "popularity_rank": popularity,
            "mal_url": a.get("url", ""),
            "post_count": scored_by,
            "sample_comments": comments,
        }

    def _empty(self, title: str) -> Dict:
        return {
            "title": title,
            "sentiment_score": None,
            "sentiment_label": "unknown",
            "mal_score": None,
            "members": 0,
            "scored_by": 0,
            "popularity_rank": None,
            "mal_url": "",
            "post_count": 0,
            "sample_comments": [],
            "from_cache": False,
        }

    def _cached(self, title: str) -> bool:
        return title in self._cache and (time.time() - self._timestamps.get(title, 0)) < self.ttl
