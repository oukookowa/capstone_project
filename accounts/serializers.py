from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'cover_photo', 'location', 'website']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Prevents exposure of passwords on client responses

    class Meta:
        model = User
        fields = ['username', 'email', 'password'] # Fields to serialize

    def create(self, validated_data):
        # Use Django's create_user() to hash the password
        user = User.objects.create_user(  # Default User model explicitly stated at the top for easy mgt
            username=validated_data['username'], 
            email=validated_data['email'],
            password=validated_data['password']  # This ensures password is hashed
        )
        # Create an authentication token for the user
        Token.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            data['user'] = user  # Explicitly add user to validated data
            return data
        raise serializers.ValidationError("Invalid credentials!")