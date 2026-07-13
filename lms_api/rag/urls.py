from django.urls import path

from .views import (
    RagConversationDetailAPIView,
    RagConversationListCreateAPIView,
    RagConversationMessageAPIView,
    RagDocumentDetailAPIView,
    RagDocumentListCreateAPIView,
    RagDocumentReindexAPIView,
    RagHealthAPIView,
)

app_name = "rag"

urlpatterns = [
    path("health/", RagHealthAPIView.as_view(), name="health"),
    path(
        "documents/",
        RagDocumentListCreateAPIView.as_view(),
        name="document-list-create",
    ),
    path(
        "documents/<int:pk>/",
        RagDocumentDetailAPIView.as_view(),
        name="document-detail",
    ),
    path(
        "documents/<int:pk>/reindex/",
        RagDocumentReindexAPIView.as_view(),
        name="document-reindex",
    ),
    path(
        "conversations/",
        RagConversationListCreateAPIView.as_view(),
        name="conversation-list-create",
    ),
    path(
        "conversations/<int:pk>/",
        RagConversationDetailAPIView.as_view(),
        name="conversation-detail",
    ),
    path(
        "conversations/<int:pk>/messages/",
        RagConversationMessageAPIView.as_view(),
        name="conversation-message",
    ),
]
