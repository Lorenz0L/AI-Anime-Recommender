import httpx
import time
from typing import List, Dict
from config.config import get_settings
from utils.logger import get_logger
from utils.exceptions import DataFetchError

logger = get_logger(__name__)
settings = get_settings()

JIKAN_BASE = "https://api.jikan.moe/v4"


class JikanDataFetcher:
    def __init__(self):
        self.limit = settings.anime_fetch_limit

    def fetch_all(self) -> List[Dict]:
        all_docs = []
        page = 1

        logger.info(f"Fetching {self.limit} anime from MyAnimeList...")

        while len(all_docs) < self.limit:
            try:
                data = self._fetch_page(page)
            except DataFetchError as e:
                logger.error(f"Stopping at page {page}: {e}")
                break

            anime_list = data.get("data", [])
            if not anime_list:
                break

            for anime in anime_list:
                doc = self._parse(anime)
                if doc:
                    all_docs.append(doc)

            has_next = data.get("pagination", {}).get("has_next_page", False)
            total_pages = data.get("pagination", {}).get("last_visible_page", "?")
            logger.info(f"Page {page}/{total_pages} — {len(all_docs)}/{self.limit} fetched")

            if not has_next:
                break

            page += 1
            time.sleep(0.4)

        logger.info(f"Fetch complete. Total: {len(all_docs)} anime")
        return all_docs

    def _fetch_page(self, page: int) -> Dict:
        try:
            with httpx.Client(timeout=15.0) as client:
                r = client.get(f"{JIKAN_BASE}/top/anime", params={"page": page, "filter": "bypopularity"})
                if r.status_code == 429:
                    logger.warning("Rate limited — waiting 3 seconds...")
                    time.sleep(3)
                    return self._fetch_page(page)
                r.raise_for_status()
                return r.json()
        except httpx.TimeoutException:
            raise DataFetchError(f"Timeout on page {page}")
        except httpx.HTTPStatusError as e:
            raise DataFetchError(f"HTTP {e.response.status_code} on page {page}")

    def _parse(self, anime: Dict) -> Dict | None:
        mal_id = anime.get("mal_id")
        title = anime.get("title", "Unknown")
        synopsis = anime.get("synopsis", "")

        if not synopsis or len(synopsis) < 50:
            return None

        genres = [g["name"] for g in anime.get("genres", [])]
        themes = [t["name"] for t in anime.get("themes", [])]
        demographics = [d["name"] for d in anime.get("demographics", [])]
        all_tags = genres + themes + demographics

        text = (
            f"Title: {title}\n"
            f"Type: {anime.get('type', 'Unknown')}\n"
            f"Tags: {', '.join(all_tags) if all_tags else 'Unknown'}\n"
            f"Episodes: {anime.get('episodes', 'Unknown')}\n"
            f"Synopsis: {synopsis[:1500]}"
        )

        return {
            "id": str(mal_id),
            "text": text,
            "metadata": {
                "mal_id": str(mal_id),
                "title": title,
                "title_english": anime.get("title_english") or title,
                "genres": ", ".join(genres) if genres else "Unknown",
                "themes": ", ".join(themes) if themes else "",
                "type": anime.get("type", "Unknown"),
                "episodes": str(anime.get("episodes", "Unknown")),
                "score": str(anime.get("score", "N/A")),
                "rank": str(anime.get("rank", "N/A")),
                "popularity": str(anime.get("popularity", "N/A")),
                "members": str(anime.get("members", 0)),
                "synopsis": synopsis[:600],
                "year": str(anime.get("year", "Unknown")),
                "status": anime.get("status", "Unknown"),
                "mal_url": anime.get("url", ""),
                "image_url": anime.get("images", {}).get("jpg", {}).get("image_url", ""),
            },
        }
