from rest_framework import serializers
from . models import Post, Comment

# Comment serializer to serialize a comment
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# Post serializer to serialize post together with comments associated with it
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        