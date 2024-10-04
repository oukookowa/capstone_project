from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response



User = get_user_model()

# Feed view to display list of Posts from a users the current user is following
class FeedView(generics.ListAPIView):
    permission_classes = [IsAuthenticated] # Permission
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        # Get the list of users the current user follows
        following_users = user.following.all()
        # Retrieve posts from those users
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    
# Custom permission to allow read for everyone and write for the owner of the object
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS: #['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.author == request.user

# View for liking a post  
class LikePostView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk) # Get instance of a post given pk
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

# View for unliking a post
class UnlikePostView(generics.DestroyAPIView):
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
    

# Implemented views using rest-framework's viewsets
# for CRUD operations for the Post model
class PostViewSet(viewsets.ModelViewSet):
    '''Function:'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author', 'content', 'created_at']  # Fields to include in filtersets
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'created_at']
    ordering = ['-created_at', '-comments_count']  # Set default ordering
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

# Viewsets for CRUD operations for the Comment model
class CommentViewSet(viewsets.ModelViewSet):
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