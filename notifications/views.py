from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

# A view that lists all notifications  associated with the current logged in user's posts
class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    # Filter through queryset to find notifications associate with a particular user
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
