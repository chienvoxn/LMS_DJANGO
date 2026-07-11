from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Prefetch
from .models import Conversation, ConversationParticipant, Message
from .serializers import (
    ConversationListSerializer,
    ConversationDetailSerializer,
    CreateConversationSerializer,
    MessageSerializer
)


class ConversationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateConversationSerializer
        return ConversationListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        return Conversation.objects.filter(
            members__user=self.request.user
        ).prefetch_related(
            Prefetch(
                'members',
                queryset=ConversationParticipant.objects.select_related('user')
            ),
            Prefetch(
                'messages',
                queryset=Message.objects.select_related('sender').order_by('-created_at')
            )
        ).distinct().order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        detail_serializer = ConversationListSerializer(
            conversation,
            context={'request': request}
        )
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class ConversationDetailView(generics.RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        return Conversation.objects.filter(
            members__user=self.request.user
        ).prefetch_related(
            Prefetch(
                'members',
                queryset=ConversationParticipant.objects.select_related('user')
            ),
            Prefetch(
                'messages',
                queryset=Message.objects.select_related('sender').order_by('created_at')
            )
        ).distinct()


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__members__user=self.request.user
        ).select_related('sender').order_by('created_at')

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = Conversation.objects.get(id=conversation_id)

        is_member = conversation.members.filter(user=self.request.user).exists()
        if not is_member:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a member of this conversation.")

        serializer.save(
            conversation=conversation,
            sender=self.request.user
        )


class ConversationUnreadCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.db.models import Max
        conversations = Conversation.objects.filter(members__user=request.user)
        count = 0
        return Response({"unread_count": count})
