# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet


router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation') # basename is used to generate reverse url name for acessing the view path 
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]