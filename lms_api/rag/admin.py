from django.contrib import admin

from .models import RagChunk, RagConversation, RagDocument, RagMessage


@admin.register(RagDocument)
class RagDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "file_type",
        "status",
        "chunk_count",
        "created_at",
    )
    list_filter = ("status", "file_type", "created_at")
    search_fields = ("name", "original_name", "owner__email")
    readonly_fields = (
        "checksum",
        "chunk_count",
        "error_message",
        "processed_at",
        "created_at",
        "updated_at",
    )


@admin.register(RagChunk)
class RagChunkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document",
        "chunk_index",
        "page_number",
        "vector_id",
    )
    search_fields = ("content", "document__name", "vector_id")
    raw_id_fields = ("document",)


class RagMessageInline(admin.TabularInline):
    model = RagMessage
    extra = 0
    readonly_fields = ("role", "content", "citations", "created_at")


@admin.register(RagConversation)
class RagConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "updated_at")
    search_fields = ("title", "owner__email")
    filter_horizontal = ("documents",)
    inlines = (RagMessageInline,)


@admin.register(RagMessage)
class RagMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "role", "model_name", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("content", "conversation__title")
    raw_id_fields = ("conversation",)
