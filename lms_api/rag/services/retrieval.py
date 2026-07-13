from .config import rag_setting
from .ollama_client import get_ollama_service
from .vector_store import get_vector_store


def retrieve_contexts(owner_id, document_ids, query):
    top_k = int(rag_setting("RAG_TOP_K", 6))
    max_distance = float(rag_setting("RAG_MAX_DISTANCE", 0.82))
    embedding = get_ollama_service().embed([query])[0]
    result = get_vector_store().query(
        owner_id=owner_id,
        document_ids=document_ids,
        query_embedding=embedding,
        top_k=top_k,
    )

    documents = (result.get("documents") or [[]])[0]
    metadatas = (result.get("metadatas") or [[]])[0]
    distances = (result.get("distances") or [[]])[0]

    contexts = []
    for content, metadata, distance in zip(documents, metadatas, distances):
        if distance is not None and float(distance) > max_distance:
            continue
        contexts.append(
            {
                "content": content,
                "distance": float(distance) if distance is not None else None,
                "metadata": metadata or {},
            }
        )
    return contexts
