from rest_framework import serializers
from . models import Post, Comment, Like
from accounts.serializers import UserSerializer

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

# Post serializer to serialize a post together with comments & likes
# associated with it
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)  # Include author field as read-only
    
    class Meta:
        model = Post
        fields = '__all__'

    # Associate a post with the authenticated user at the instance a post is created
    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(author=request.user, **validated_data)
        return post
        
    # The above method is also achievable by using perform_create in the views i.e 
    # def perform_create(self, serializer):
        # This method will call the create method in the serializer
        # serializer.save(author=self.request.user)

