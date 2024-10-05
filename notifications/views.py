from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    '''
    Function: Lists all notifications that have the current logged in user as the recipient
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    # Filter through queryset to find notifications associated with a particular user
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
