import time

from django.db import transaction
from django.utils import timezone

from rag.models import RagDocument, RagMessage

from .exceptions import RagError
from .ollama_client import get_ollama_service
from .prompts import SYSTEM_PROMPT, build_user_prompt
from .retrieval import retrieve_contexts


NO_CONTEXT_ANSWER = (
    "Tôi chưa tìm thấy thông tin đủ liên quan trong các tài liệu đã chọn. "
    "Bạn có thể chọn thêm tài liệu hoặc đặt câu hỏi cụ thể hơn."
)


def _citation_list(contexts):
    citations = []
    seen = set()
    for index, item in enumerate(contexts, start=1):
        metadata = item["metadata"]
        key = (
            metadata.get("document_id"),
            metadata.get("page_number"),
            metadata.get("chunk_index"),
        )
        if key in seen:
            continue
        seen.add(key)
        citations.append(
            {
                "source_number": index,
                "document_id": metadata.get("document_id"),
                "document_name": metadata.get("document_name", "Tài liệu"),
                "page_number": metadata.get("page_number"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": item.get("distance"),
            }
        )
    return citations


def _history_messages(conversation, limit=8):
    messages = list(conversation.messages.order_by("-created_at", "-id")[:limit])
    messages.reverse()
    return [
        {"role": item.role, "content": item.content}
        for item in messages
        if item.role in {RagMessage.Role.USER, RagMessage.Role.ASSISTANT}
    ]


def answer_question(conversation, question):
    ready_documents = list(
        conversation.documents.filter(
            owner=conversation.owner,
            status=RagDocument.Status.READY,
        )
    )
    if not ready_documents:
        raise RagError(
            "Hãy chọn ít nhất một tài liệu có trạng thái ready trước khi hỏi."
        )

    document_ids = [item.id for item in ready_documents]
    contexts = retrieve_contexts(
        owner_id=conversation.owner_id,
        document_ids=document_ids,
        query=question,
    )
    history = _history_messages(conversation)
    started = time.perf_counter()

    if contexts:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {
                "role": "user",
                "content": build_user_prompt(question, contexts),
            },
        ]
        answer = get_ollama_service().chat(messages)
        citations = _citation_list(contexts)
    else:
        answer = NO_CONTEXT_ANSWER
        citations = []

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    model_name = get_ollama_service().llm_model

    with transaction.atomic():
        user_message = RagMessage.objects.create(
            conversation=conversation,
            role=RagMessage.Role.USER,
            content=question,
        )
        assistant_message = RagMessage.objects.create(
            conversation=conversation,
            role=RagMessage.Role.ASSISTANT,
            content=answer,
            citations=citations,
            model_name=model_name,
            response_time_ms=elapsed_ms,
        )

        update_fields = ["updated_at"]
        conversation.updated_at = timezone.now()
        if conversation.title == "New chat" or not conversation.title.strip():
            conversation.title = question[:80]
            update_fields.append("title")
        conversation.save(update_fields=update_fields)

    return {
        "conversation_id": conversation.id,
        "answer": answer,
        "citations": citations,
        "user_message": {
            "id": user_message.id,
            "role": user_message.role,
            "content": user_message.content,
            "citations": [],
            "created_at": user_message.created_at,
        },
        "assistant_message": {
            "id": assistant_message.id,
            "role": assistant_message.role,
            "content": assistant_message.content,
            "citations": assistant_message.citations,
            "model_name": assistant_message.model_name,
            "response_time_ms": assistant_message.response_time_ms,
            "created_at": assistant_message.created_at,
        },
    }
