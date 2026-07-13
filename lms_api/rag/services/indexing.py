import hashlib
from pathlib import Path

from django.db import transaction
from django.utils import timezone

from rag.models import RagChunk, RagDocument

from .chunker import chunk_units
from .config import rag_setting
from .document_parser import parse_document
from .ollama_client import get_ollama_service
from .vector_store import get_vector_store


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def delete_document_index(document):
    get_vector_store().delete_document(
        owner_id=document.owner_id,
        document_id=document.id,
    )
    RagChunk.objects.filter(document=document).delete()


def index_document(document):
    if not document.file:
        raise ValueError("Document không có file.")

    RagDocument.objects.filter(pk=document.pk).update(
        status=RagDocument.Status.PROCESSING,
        error_message="",
        chunk_count=0,
        processed_at=None,
    )
    document.refresh_from_db()

    try:
        path = Path(document.file.path)
        checksum = _sha256(path)
        units = parse_document(path, document.file_type)
        chunks = chunk_units(
            units,
            size=int(rag_setting("RAG_CHUNK_SIZE", 1000)),
            overlap=int(rag_setting("RAG_CHUNK_OVERLAP", 180)),
        )
        if not chunks:
            raise ValueError("Không tạo được chunk nào từ tài liệu.")

        delete_document_index(document)

        ollama = get_ollama_service()
        vector_store = get_vector_store()
        batch_size = 16
        db_chunks = []

        for start in range(0, len(chunks), batch_size):
            batch = chunks[start : start + batch_size]
            texts = [item.content for item in batch]
            embeddings = ollama.embed(texts)
            ids = [
                f"doc-{document.id}-chunk-{item.chunk_index}"
                for item in batch
            ]
            metadatas = []
            for item in batch:
                metadata = {
                    "owner_id": int(document.owner_id),
                    "document_id": int(document.id),
                    "document_name": document.name,
                    "chunk_index": int(item.chunk_index),
                    "file_type": document.file_type,
                }
                if item.page_number is not None:
                    metadata["page_number"] = int(item.page_number)
                if item.section_title:
                    metadata["section_title"] = item.section_title
                metadatas.append(metadata)

            vector_store.upsert(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
            )

            for vector_id, item, metadata in zip(ids, batch, metadatas):
                db_chunks.append(
                    RagChunk(
                        document=document,
                        vector_id=vector_id,
                        chunk_index=item.chunk_index,
                        content=item.content,
                        page_number=item.page_number,
                        section_title=item.section_title,
                        metadata=metadata,
                    )
                )

        with transaction.atomic():
            RagChunk.objects.bulk_create(db_chunks, batch_size=500)
            RagDocument.objects.filter(pk=document.pk).update(
                checksum=checksum,
                status=RagDocument.Status.READY,
                chunk_count=len(chunks),
                error_message="",
                processed_at=timezone.now(),
            )
        document.refresh_from_db()
        return document

    except Exception as exc:
        try:
            delete_document_index(document)
        except Exception:
            # Không che mất lỗi gốc nếu Chroma cũng đang lỗi.
            pass
        RagDocument.objects.filter(pk=document.pk).update(
            status=RagDocument.Status.FAILED,
            chunk_count=0,
            error_message=str(exc)[:4000],
            processed_at=None,
        )
        document.refresh_from_db()
        raise
