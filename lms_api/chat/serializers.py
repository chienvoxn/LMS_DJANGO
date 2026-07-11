from rest_framework import serializers
from django.db.models import Q
from .models import Conversation, ConversationParticipant, Message
from users.models import User


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'avatar_url', 'role']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserBriefSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'created_at']


class ConversationListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    display_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'is_group', 'name', 'display_name', 'display_avatar', 'last_message', 'member_count', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        msgs = getattr(obj, '_prefetched_objects_cache', {}).get('messages')
        if msgs is not None:
            ordered = sorted(msgs, key=lambda m: m.created_at, reverse=True)
            last_msg = ordered[0] if ordered else None
        else:
            last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_member_count(self, obj):
        return obj.members.count()

    def get_display_name(self, obj):
        if obj.is_group and obj.name:
            return obj.name
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            other = obj.members.exclude(user=request.user).first()
            if other:
                return other.user.full_name or other.user.email
        return obj.name or f"Conversation {obj.id}"

    def get_display_avatar(self, obj):
        if obj.is_group:
            return None
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            other = obj.members.exclude(user=request.user).first()
            if other:
                return other.user.avatar_url
        return None


class ConversationDetailSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    display_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'is_group', 'name', 'display_name', 'display_avatar', 'members', 'messages', 'created_at', 'updated_at']

    def get_members(self, obj):
        participants = obj.members.select_related('user').all()
        return [UserBriefSerializer(p.user).data for p in participants]

    def get_messages(self, obj):
        msgs = obj.messages.select_related('sender').order_by('created_at')
        return MessageSerializer(msgs, many=True).data

    def get_display_name(self, obj):
        if obj.is_group and obj.name:
            return obj.name
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            other = obj.members.exclude(user=request.user).first()
            if other:
                return other.user.full_name or other.user.email
        return obj.name or f"Conversation {obj.id}"

    def get_display_avatar(self, obj):
        if obj.is_group:
            return None
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            other = obj.members.exclude(user=request.user).first()
            if other:
                return other.user.avatar_url
        return None


class CreateConversationSerializer(serializers.Serializer):
    emails = serializers.ListField(
        child=serializers.EmailField(),
        allow_empty=False,
        write_only=True
    )

    def validate_emails(self, value):
        existing_emails = set(User.objects.filter(email__in=value).values_list('email', flat=True))
        invalid = set(value) - existing_emails
        if invalid:
            raise serializers.ValidationError(f"Emails not found: {', '.join(invalid)}")
        return value

    def _ensure_participants(self, conversation, users):
        existing_user_ids = set(
            conversation.members.values_list('user_id', flat=True)
        )
        new_participants = [
            ConversationParticipant(conversation=conversation, user=user)
            for user in users
            if user.id not in existing_user_ids
        ]
        if new_participants:
            ConversationParticipant.objects.bulk_create(new_participants)

    def create(self, validated_data):
        emails = validated_data['emails']
        users = list(User.objects.filter(email__in=emails))
        request = self.context.get('request')
        creator = request.user

        if creator not in users:
            users.append(creator)

        existing = None
        if len(users) == 2:
            existing = Conversation.objects.filter(is_group=False).filter(
                members__user=users[0]
            ).filter(
                members__user=users[1]
            ).distinct().first()

        if existing:
            self._ensure_participants(existing, users)
            return existing

        is_group = len(users) > 2
        conversation = Conversation.objects.create(
            is_group=is_group,
            name=None if not is_group else f"Group ({len(users)})"
        )

        participants = [
            ConversationParticipant(conversation=conversation, user=user)
            for user in users
        ]
        ConversationParticipant.objects.bulk_create(participants)

        return conversation
