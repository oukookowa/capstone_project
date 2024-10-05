from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    '''
    Function: Allows authenticated users to create, update, retrieve a conversation with one or more other users
    '''
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        # Show only conversations the user is a participant of
        return self.request.user.conversations.all()
    
class MessageViewSet(viewsets.ModelViewSet):
    '''
    Function: Allows a user to send a message to another user within a given conversation
    '''
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve messages only for conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)