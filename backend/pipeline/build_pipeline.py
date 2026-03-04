from src.data_fetcher import JikanDataFetcher
from src.vector_store import AnimeVectorStore
from utils.logger import get_logger

logger = get_logger("build_pipeline")


def main():
    logger.info("AniMind — Build Pipeline Starting")

    store = AnimeVectorStore()

    if store.is_populated():
        logger.info("Database already built. Delete 'chroma_db' folder to rebuild.")
        return

    fetcher = JikanDataFetcher()
    documents = fetcher.fetch_all()

    if not documents:
        logger.error("No anime fetched. Check your internet connection.")
        return

    store.get_or_create_collection()
    store.add_documents(documents)

    logger.info(f"Done. {len(documents)} anime in database.")
    logger.info("Start the app: uvicorn app.main:app --reload --port 8000")


if __name__ == "__main__":
    main()
