# © 2024 Ouko Okowa
# Licensed under the MIT License. See LICENSE file for details.

from rest_framework import serializers
from . models import Post, Comment, Like, Repost, Hashtag
from accounts.serializers import UserSerializer
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

# Comment serializer to serialize a comment
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Include author field as read-only
    
    class Meta:
        model = Comment
        fields = '__all__'

    # Associate a comment with the authenticated user at the instance
    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(author=request.user, **validated_data)
        return comment

# Like serializer to serialize a like
class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Include author field as read-only
    class Meta:
        model = Like
        fields = '__all__'

    # Associate a like with the authenticated user at the instance
    def create(self, validated_data):
        request = self.context.get('request')
        like = Like.objects.create(author=request.user, **validated_data)
        return like

class RepostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Repost
        fields = ['original_post', 'user', 'created_at', 'comment']

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name']

# Post serializer to serialize a post together with comments & likes
# associated with it
class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)  # Include author field details as read-only
    reposts = RepostSerializer(many=True, read_only=True)
    mentions = UserSerializer(many=True, read_only=True)  # To display full user info for mentions
    hashtags = HashtagSerializer(many=True, read_only=True)
    tags = TagListSerializerField() # Holds the tags associated with an instance of a post

    class Meta:
        model = Post
        fields = '__all__'

    # Associate a post with the authenticated user at the instance a post is created
    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags', [])  # Pop tags from validated data
        post = Post.objects.create(author=request.user, **validated_data) # Set author
        post.tags.set(tags)  # Add respective tags to the post instance explicitly
        return post
        
    ''' 
    The above method is also achievable by using perform_create in the views i.e 
    def perform_create(self, serializer):
        This method will call the create method in the serializer
        serializer.save(author=self.request.user)
    '''
