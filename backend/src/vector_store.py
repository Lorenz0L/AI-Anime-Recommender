import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
from config.config import get_settings
from utils.logger import get_logger
from utils.exceptions import VectorStoreError

logger = get_logger(__name__)
settings = get_settings()

COLLECTION_NAME = "anime_collection"


class AnimeVectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_db_path)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.embedding_model
        )
        self.collection = None

    def get_or_create_collection(self):
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(f"ChromaDB ready — {self.collection.count()} anime stored")
        return self.collection

    def is_populated(self) -> bool:
        try:
            col = self.client.get_collection(name=COLLECTION_NAME)
            return col.count() > 0
        except Exception:
            return False

    def add_documents(self, documents: List[Dict], batch_size: int = 100):
        if self.collection is None:
            self.get_or_create_collection()

        total = len(documents)
        logger.info(f"Embedding {total} anime into ChromaDB...")

        for i in range(0, total, batch_size):
            batch = documents[i: i + batch_size]
            try:
                self.collection.add(
                    ids=[d["id"] for d in batch],
                    documents=[d["text"] for d in batch],
                    metadatas=[d["metadata"] for d in batch],
                )
                logger.info(f"  {min(i + batch_size, total)}/{total} embedded")
            except Exception as e:
                raise VectorStoreError(f"Failed at batch {i}: {e}")

        logger.info("All anime saved to ChromaDB.")

    def query(self, query_text: str, n_results: int = None) -> List[Dict]:
        if self.collection is None:
            self.get_or_create_collection()

        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results or settings.top_k_results,
                include=["metadatas", "distances"],
            )
        except Exception as e:
            raise VectorStoreError(f"Query failed: {e}")

        return [
            {**meta, "similarity_score": round(1 - dist, 4)}
            for meta, dist in zip(results["metadatas"][0], results["distances"][0])
        ]
