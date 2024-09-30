from django.urls import path, include
from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, UnlikePostView
from rest_framework.routers import DefaultRouter


# Create a router to register the viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet) # Registers postviewset
router.register(r'comments', CommentViewSet) # Registers commentviewset


# API urls are generated automatically by the router
urlpatterns = [
    path('',include(router.urls)),
    path('posts/feed/', FeedView.as_view(), name='user-feed'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]