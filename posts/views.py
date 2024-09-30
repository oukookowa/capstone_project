from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from notifications.models import Notification


User = get_user_model()

# Feed view to display list of Posts from a users the current user is following
class FeedView(generics.ListAPIView):
    permission_classes = [IsAuthenticated] #permissions.IsAuthenticated
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
        return obj.owner == request.user

# View for liking a post  
class LikePostView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk) #generics.get_object_or_404(Post, pk=pk) ->IDK why checker needs this
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            # Create a notification
            Notification.objects.create(
                recipient=post.user,
                actor=request.user,
                verb='liked your post',
                target=post
            )
            return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

# View for unliking a post
class UnlikePostView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
    
'''# For practice purposes, here's implementation of the views using generics API views
# List all posts
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_class = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author', 'created_at']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'created_at']


# Retrieve a post based on its ID
class PostDetailView(generics.RetrieveApiView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_class = [IsAuthenticatedOrReadOnly]

# Adding a new post
class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated]

# Updating a post based on its ID
class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.ojects.all()
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated]

# Deleting a post based on its ID
class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_class = [IsAuthenticated]

# List all comments
class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author', 'created_at']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'created_at']

# Retrieve a comment based on its ID
class CommentDetailView(generics.RetrieveApiView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticatedOrReadOnly]

# Adding a new comment
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticated]

# Updating a comment based on its ID
class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.ojects.all()
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticated]

# Deleting a comment based on its ID
class BookDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_class = [IsOwnerOrReadOnly]
'''

# Implemented views using rest-framework's viewsets

# Viewsets for CRUD operations for the Post model
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author', 'content', 'created_at']
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'created_at']
    permission_classes = [IsAuthenticated, IsAdminUser, IsOwnerOrReadOnly]

    # Overide get permissions to dynamically set permissions
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

# Viewsets for CRUD operations for the Comment model
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, IsOwnerOrReadOnly]

    # Overide get permissions to dynamically set permissions
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action == 'detail':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]