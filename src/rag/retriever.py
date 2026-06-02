import chromadb
from chromadb.utils import embedding_functions
from src.config import CHROMA_PERSIST_DIR, COLLECTION_NAME, EMBEDDING_MODEL


class KBRetriever:
    def __init__(self):
        client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
        self.collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embed_fn,
        )

    def retrieve(self, query: str, k: int = 3, category: str = None):
        where = None
        if category and category not in ["general", None]:
            where = {"category": category}

        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=where,
        )
        docs = results["documents"][0] if results["documents"] else []
        metas = results["metadatas"][0] if results["metadatas"] else []
        return [{"content": d, "metadata": m} for d, m in zip(docs, metas)]
