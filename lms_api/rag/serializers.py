from pathlib import Path

from django.conf import settings
from rest_framework import serializers

from .models import RagConversation, RagDocument, RagMessage


class RagDocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = RagDocument
        fields = (
            "id",
            "name",
            "original_name",
            "file",
            "file_url",
            "file_type",
            "mime_type",
            "size_bytes",
            "checksum",
            "status",
            "chunk_count",
            "error_message",
            "processed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "original_name",
            "file_url",
            "file_type",
            "mime_type",
            "size_bytes",
            "checksum",
            "status",
            "chunk_count",
            "error_message",
            "processed_at",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"name": {"required": False}}

    def get_file_url(self, obj):
        if not obj.file:
            return None
        request = self.context.get("request")
        url = obj.file.url
        return request.build_absolute_uri(url) if request else url

    def validate_file(self, uploaded_file):
        extension = Path(uploaded_file.name).suffix.lower().lstrip(".")
        allowed = getattr(
            settings,
            "RAG_ALLOWED_EXTENSIONS",
            ["pdf", "txt", "docx", "pptx"],
        )
        if extension not in allowed:
            raise serializers.ValidationError(
                f"Định dạng .{extension or 'unknown'} chưa được hỗ trợ. "
                f"Cho phép: {', '.join(allowed)}."
            )

        max_mb = int(getattr(settings, "RAG_MAX_FILE_SIZE_MB", 30))
        if uploaded_file.size > max_mb * 1024 * 1024:
            raise serializers.ValidationError(
                f"Tệp vượt quá giới hạn {max_mb} MB."
            )
        if uploaded_file.size == 0:
            raise serializers.ValidationError("Tệp tải lên đang rỗng.")
        return uploaded_file

    def create(self, validated_data):
        uploaded_file = validated_data["file"]
        extension = Path(uploaded_file.name).suffix.lower().lstrip(".")
        default_name = Path(uploaded_file.name).stem[:255]
        return RagDocument.objects.create(
            owner=self.context["request"].user,
            name=validated_data.get("name") or default_name,
            original_name=uploaded_file.name[:255],
            file=uploaded_file,
            file_type=extension,
            mime_type=getattr(uploaded_file, "content_type", "") or "",
            size_bytes=uploaded_file.size,
        )


class RagDocumentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = RagDocument
        fields = (
            "id",
            "name",
            "original_name",
            "file_type",
            "status",
            "chunk_count",
            "created_at",
        )


class RagMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RagMessage
        fields = (
            "id",
            "role",
            "content",
            "citations",
            "model_name",
            "response_time_ms",
            "created_at",
        )
        read_only_fields = fields


class RagConversationListSerializer(serializers.ModelSerializer):
    documents = RagDocumentSummarySerializer(many=True, read_only=True)
    message_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = RagConversation
        fields = (
            "id",
            "title",
            "documents",
            "message_count",
            "created_at",
            "updated_at",
        )


class RagConversationDetailSerializer(serializers.ModelSerializer):
    documents = RagDocumentSummarySerializer(many=True, read_only=True)
    messages = RagMessageSerializer(many=True, read_only=True)

    class Meta:
        model = RagConversation
        fields = (
            "id",
            "title",
            "documents",
            "messages",
            "created_at",
            "updated_at",
        )


class RagConversationWriteSerializer(serializers.ModelSerializer):
    document_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        allow_empty=True,
        write_only=True,
    )

    class Meta:
        model = RagConversation
        fields = ("id", "title", "document_ids", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
        extra_kwargs = {"title": {"required": False}}

    def validate_document_ids(self, ids):
        unique_ids = list(dict.fromkeys(ids))
        user = self.context["request"].user
        found = RagDocument.objects.filter(owner=user, id__in=unique_ids)
        if found.count() != len(unique_ids):
            raise serializers.ValidationError(
                "Có tài liệu không tồn tại hoặc không thuộc tài khoản của bạn."
            )
        return unique_ids

    def create(self, validated_data):
        document_ids = validated_data.pop("document_ids", [])
        conversation = RagConversation.objects.create(
            owner=self.context["request"].user,
            **validated_data,
        )
        if document_ids:
            conversation.documents.set(
                RagDocument.objects.filter(
                    owner=conversation.owner,
                    id__in=document_ids,
                )
            )
        return conversation

    def update(self, instance, validated_data):
        document_ids = validated_data.pop("document_ids", None)
        instance = super().update(instance, validated_data)
        if document_ids is not None:
            instance.documents.set(
                RagDocument.objects.filter(
                    owner=instance.owner,
                    id__in=document_ids,
                )
            )
        return instance


class RagQuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=10000, trim_whitespace=True)
    document_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        allow_empty=False,
    )

    def validate_question(self, value):
        if not value.strip():
            raise serializers.ValidationError("Câu hỏi không được để trống.")
        return value.strip()

    def validate_document_ids(self, value):
        return list(dict.fromkeys(value))
