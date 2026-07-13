from functools import lru_cache
from pathlib import Path

import chromadb

from .config import rag_setting


class VectorStore:
    def __init__(self):
        path = Path(rag_setting("RAG_CHROMA_PATH", "./chroma_db"))
        path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(path))
        self.collection = self.client.get_or_create_collection(
            name=rag_setting(
                "RAG_COLLECTION_NAME",
                "lms_user_documents",
            ),
            metadata={"hnsw:space": "cosine"},
        )

    @staticmethod
    def _where(owner_id, document_ids=None):
        conditions = [{"owner_id": {"$eq": int(owner_id)}}]
        if document_ids:
            ids = [int(item) for item in document_ids]
            if len(ids) == 1:
                conditions.append({"document_id": {"$eq": ids[0]}})
            else:
                conditions.append({"document_id": {"$in": ids}})
        return conditions[0] if len(conditions) == 1 else {"$and": conditions}

    def upsert(self, *, ids, documents, embeddings, metadatas):
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def delete_document(self, owner_id, document_id):
        self.collection.delete(
            where=self._where(owner_id, [document_id])
        )

    def query(self, *, owner_id, document_ids, query_embedding, top_k):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=self._where(owner_id, document_ids),
            include=["documents", "metadatas", "distances"],
        )

    def heartbeat(self):
        return self.client.heartbeat()


@lru_cache(maxsize=1)
def get_vector_store():
    return VectorStore()
