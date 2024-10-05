from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status

class IsParticipant(BasePermission):
    '''
    Custom permission to only allow participants of a conversation to perform CRUD operations.
    '''
    def has_object_permission(self, request, view, obj):
        # Assuming the 'Conversation' model has a ManyToMany field called 'participants'
        # and the authenticated user is stored in `request.user`
        return request.user in obj.participants.all()

class IsMessageParticipant(BasePermission):
    '''
    Custom permission to only allow participants of a conversation to perform CRUD operations on messages.
    '''
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation related to this message
        return request.user in obj.conversation.participants.all()

class ConversationViewSet(viewsets.ModelViewSet):
    '''
    Function: Allows authenticated users to create, update, retrieve a conversation with one or more other users
    '''
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]

    # Overide get permissions to dynamically set permissions
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsParticipant]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsParticipant]
        else:
            permission_classes = [IsAuthenticated, IsParticipant]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Show only conversations the user is a participant of
        return self.request.user.conversations.all()
    
class MessageViewSet(viewsets.ModelViewSet):
    '''
    Function: Allows a user to send a message to another user within a given conversation
    '''
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageParticipant]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsMessageParticipant]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsMessageParticipant]
        else:
            permission_classes = [IsAuthenticated, IsMessageParticipant]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Retrieve messages only for conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)