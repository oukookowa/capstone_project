from django.urls import path, include
from .views import (PostViewSet, CommentViewSet, FeedView, 
                    LikePostView, UnlikePostView, RepostView, 
                    HashtagPostsView, MentionedPostsView, 
                    TagPostsView, TrendingPostView)
from rest_framework.routers import DefaultRouter


# Create a router to register the viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet) # Registers postviewset
router.register(r'comments', CommentViewSet) # Registers commentviewset


# API urls for viewsets are generated automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='user-feed'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('posts/<int:post_id>/reposts/', RepostView.as_view(), name='repost-post'),
    path('posts/hashtag/<str:hashtag>/', HashtagPostsView.as_view(), name='hashtag-posts'),
    path('posts/mention/<str:username>/', MentionedPostsView.as_view(), name='mentioned-posts'),
    path('posts/tag/<str:tag>/', TagPostsView.as_view(), name='tag-posts'),
    path('trending/', TrendingPostView.as_view(), name='trending-posts')
]