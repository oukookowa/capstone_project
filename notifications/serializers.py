from rest_framework import serializers
from .models import Notification
from messages.serializers import MessageSerializer
from posts.serializers import CommentSerializer, LikeSerializer
from django.contrib.contenttypes.models import ContentType
from posts.models import Like, Comment
from messages.models import Message

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()  # Display actor's username
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target', 'timestamp', 'read']

    def get_target(self, obj):
        content_type = obj.target_content_type

        if content_type == ContentType.objects.get_for_model(Like):
            return LikeSerializer(obj.target).data
        elif content_type == ContentType.objects.get_for_model(Comment):
            return CommentSerializer(obj.target).data
        elif content_type == ContentType.objects.get_for_model(Message):
            return MessageSerializer(obj.target).data
        return None