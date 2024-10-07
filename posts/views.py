from django.shortcuts import render
from rest_framework import viewsets, generics, status, serializers
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Post, Comment, Like, Repost
from .serializers import PostSerializer, RepostSerializer, CommentSerializer, LikeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import logging

# Get default auth user model
User = get_user_model()

class FeedView(generics.ListAPIView):
    '''
    Function: Displays list of Posts from a users the current user is following
    '''
    permission_classes = [IsAuthenticated] # Permission
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        # Get the list of users the current user follows
        followed_users = user.following.all()
        # Retrieve posts from those users
        return Post.objects.filter(author__in=followed_users).order_by('-created_at')
    
class IsOwnerOrReadOnly(BasePermission):
    '''
    Function: A custom permission to allow read from anyone and write for the owner of the object
    '''
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS: #['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.author == request.user

class LikePostView(generics.CreateAPIView):
    '''
    Function: Allows authenticated users to like a post
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk) # Get instance of a post given pk
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostView(generics.DestroyAPIView):
    '''
    Function: Allows authenticated users to unlike a post that they have liked
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
    
class PostViewSet(viewsets.ModelViewSet):
    '''
    Function: Allows users to see a list of all posts and retrieve post detail,
    authenticated users to create a post and retrieve post detail, 
    post owners to update or delete a post
    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author', 'content', 'created_at']  # Fields to include in filtersets
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'created_at', 'comments_count']
    ordering = ['-created_at']  # Set default ordering
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # Overide get permissions to dynamically set permissions
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

class CommentViewSet(viewsets.ModelViewSet):
    '''
    Function: Allows users to see a list of all comments and retrieve comment detail,
    authenticated users to create a comment and retrieve comment detail, 
    post owners to update or delete a comment
    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'content', 'created_at', 'updated_at']
    search_fields = ['content', 'author__username']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']  # Set default ordering


    # Overide get permissions to dynamically set permissions
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'detail':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
    
class RepostView(generics.GenericAPIView):
    '''
    Function: Allows a user to create a repost for an existing post,
    and allows for querying to list the reposts
    '''
    serializer_class = RepostSerializer
    permission_class = [IsAuthenticated]
    queryset = Repost.objects.all()

    def get(self, request, post_id):
        # List all reposts for a specific post
        reposts = self.queryset.filter(original_post__id=post_id)
        serializer = self.get_serializer(reposts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        # Access the post_id from the URL kwargs
        try:
            original_post = get_object_or_404(Post, pk=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create the repost
        repost = Repost.objects.create(original_post=original_post, user=request.user)
        return Response(RepostSerializer(repost).data, status=status.HTTP_201_CREATED)