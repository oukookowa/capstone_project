from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model() # Retrieve the auth_user model being used by django

# Message serializer to serialize an instance of a message
class MessageSerializer(serializers.ModelSerializer):
    # Sender will be read only so that data is assigned to user issuing request
    sender = serializers.ReadOnlyField(source='sender.username')  

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'content', 'created_at']

    # Associate a message with the authenticated user at the instance
    def create(self, validated_data):
        request = self.context.get('request')
        message = Message.objects.create(sender=request.user, **validated_data)
        return message

# Conversation serializer to serialize an instance of a message
class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    # Explicitly specify the username field as a slug for the User model. Extracts only username of participants not all object attributes
    participants = serializers.SlugRelatedField(
        many=True, 
        slug_field='username', 
        read_only=True
        )
    # Write-only field for participant usernames (not shown in the output)
    participant_usernames = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    class Meta:
        model = Conversation
        fields = [
            'id',
            'participants', 
            'participant_usernames', 
            'messages', 
            'created_at'
            ]

    # Associate a conversation with the authenticated user who sends message and the other participants intednded to receive the message
    def create(self, validated_data):
        # Extract participant usernames from input data
        participant_usernames = validated_data.pop('participant_usernames')

        # Automatically include the current user in the list of participants
        participant_usernames.append(self.context['request'].user.username)

        # Retrieve User objects for the given usernames
        participants = User.objects.filter(username__in=participant_usernames)
        
        if participants.count() != len(participant_usernames):
            raise serializers.ValidationError("One or more participants do not exist.")

        # Create the conversation instance
        conversation = Conversation.objects.create()

        # Set the participants (assigns all at once, clearing any previous ones if necessary)
        conversation.participants.set(participants)

        return conversation