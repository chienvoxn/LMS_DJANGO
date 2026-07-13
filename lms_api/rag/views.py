import logging

from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RagConversation, RagDocument
from .serializers import (
    RagConversationDetailSerializer,
    RagConversationListSerializer,
    RagConversationWriteSerializer,
    RagDocumentSerializer,
    RagQuestionSerializer,
)
from .services.exceptions import RagError, RagServiceUnavailable
from .services.indexing import delete_document_index, index_document
from .services.ollama_client import get_ollama_service
from .services.rag_service import answer_question
from .services.vector_store import get_vector_store

logger = logging.getLogger(__name__)


class RagHealthAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = {
            "status": "ok",
            "ollama": False,
            "chroma": False,
        }
        errors = {}

        try:
            get_ollama_service().health()
            result["ollama"] = True
        except Exception as exc:  # pragma: no cover - phụ thuộc service ngoài
            errors["ollama"] = str(exc)

        try:
            get_vector_store().heartbeat()
            result["chroma"] = True
        except Exception as exc:  # pragma: no cover
            errors["chroma"] = str(exc)

        if errors:
            result["status"] = "degraded"
            result["errors"] = errors
            return Response(result, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(result)


class RagDocumentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RagDocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return RagDocument.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()

        try:
            index_document(document)
        except Exception:
            # index_document đã lưu status=failed và error_message.
            logger.exception("Không thể index RAG document %s", document.id)

        document.refresh_from_db()
        output = RagDocumentSerializer(document, context={"request": request})
        return Response(output.data, status=status.HTTP_201_CREATED)


class RagDocumentDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = RagDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RagDocument.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        storage = instance.file.storage
        file_name = instance.file.name
        delete_document_index(instance)
        instance.delete()
        if file_name and storage.exists(file_name):
            storage.delete(file_name)


class RagDocumentReindexAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        document = get_object_or_404(
            RagDocument,
            pk=pk,
            owner=request.user,
        )
        try:
            index_document(document)
        except Exception:
            logger.exception("Re-index thất bại cho document %s", document.id)

        document.refresh_from_db()
        serializer = RagDocumentSerializer(document, context={"request": request})
        response_status = (
            status.HTTP_200_OK
            if document.status == RagDocument.Status.READY
            else status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        return Response(serializer.data, status=response_status)


class RagConversationListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            RagConversation.objects.filter(owner=self.request.user)
            .prefetch_related("documents")
            .annotate(message_count=Count("messages"))
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return RagConversationWriteSerializer
        return RagConversationListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        output = RagConversationDetailSerializer(conversation)
        return Response(output.data, status=status.HTTP_201_CREATED)


class RagConversationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            RagConversation.objects.filter(owner=self.request.user)
            .prefetch_related("documents", "messages")
        )

    def get_serializer_class(self):
        if self.request.method in {"PATCH", "PUT"}:
            return RagConversationWriteSerializer
        return RagConversationDetailSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = RagConversationWriteSerializer(
            instance,
            data=request.data,
            partial=partial,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(RagConversationDetailSerializer(conversation).data)


class RagConversationMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        conversation = get_object_or_404(
            RagConversation.objects.prefetch_related("documents", "messages"),
            pk=pk,
            owner=request.user,
        )
        serializer = RagQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.validated_data["question"]
        document_ids = serializer.validated_data.get("document_ids")

        if document_ids is not None:
            documents = RagDocument.objects.filter(
                owner=request.user,
                id__in=document_ids,
            )
            if documents.count() != len(document_ids):
                return Response(
                    {
                        "detail": (
                            "Có tài liệu không tồn tại hoặc không thuộc "
                            "tài khoản của bạn."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            conversation.documents.set(documents)

        try:
            result = answer_question(conversation, question)
        except RagServiceUnavailable as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except RagError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(result, status=status.HTTP_201_CREATED)
