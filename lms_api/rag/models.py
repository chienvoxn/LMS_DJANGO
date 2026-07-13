import uuid
from pathlib import Path

from django.conf import settings
from django.db import models


def rag_document_upload_to(instance, filename):
    extension = Path(filename).suffix.lower()
    safe_name = f"{uuid.uuid4().hex}{extension}"
    owner_id = instance.owner_id or "unknown"
    return f"rag/documents/{owner_id}/{safe_name}"


class RagDocument(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        READY = "ready", "Ready"
        FAILED = "failed", "Failed"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rag_documents",
    )
    name = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=rag_document_upload_to)
    file_type = models.CharField(max_length=20)
    mime_type = models.CharField(max_length=120, blank=True)
    size_bytes = models.PositiveBigIntegerField(default=0)
    checksum = models.CharField(max_length=64, blank=True, db_index=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    chunk_count = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["owner", "status"],
                name="rag_doc_owner_status_idx",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.owner_id})"


class RagChunk(models.Model):
    document = models.ForeignKey(
        RagDocument,
        on_delete=models.CASCADE,
        related_name="chunks",
    )
    vector_id = models.CharField(max_length=100, unique=True)
    chunk_index = models.PositiveIntegerField()
    content = models.TextField()
    page_number = models.PositiveIntegerField(null=True, blank=True)
    section_title = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["chunk_index"]
        constraints = [
            models.UniqueConstraint(
                fields=["document", "chunk_index"],
                name="rag_unique_document_chunk",
            ),
        ]
        indexes = [
            models.Index(
                fields=["document", "chunk_index"],
                name="rag_chunk_doc_index_idx",
            ),
        ]

    def __str__(self):
        return f"Document {self.document_id} - chunk {self.chunk_index}"


class RagConversation(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rag_conversations",
    )
    title = models.CharField(max_length=255, default="New chat")
    documents = models.ManyToManyField(
        RagDocument,
        related_name="rag_conversations",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(
                fields=["owner", "updated_at"],
                name="rag_conv_owner_updated_idx",
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.owner_id})"


class RagMessage(models.Model):
    class Role(models.TextChoices):
        USER = "user", "User"
        ASSISTANT = "assistant", "Assistant"

    conversation = models.ForeignKey(
        RagConversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    content = models.TextField()
    citations = models.JSONField(default=list, blank=True)
    model_name = models.CharField(max_length=100, blank=True)
    response_time_ms = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]
        indexes = [
            models.Index(
                fields=["conversation", "created_at"],
                name="rag_msg_conv_created_idx",
            ),
        ]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
