from django.urls import path
from . import views

urlpatterns = [
    path('chat/conversations/', views.ConversationListCreateView.as_view(), name='chat-conversations'),
    path('chat/conversations/<int:pk>/', views.ConversationDetailView.as_view(), name='chat-conversation-detail'),
    path('chat/conversations/<int:conversation_id>/messages/', views.MessageListCreateView.as_view(), name='chat-messages'),
    path('chat/unread-count/', views.ConversationUnreadCountView.as_view(), name='chat-unread-count'),
]
