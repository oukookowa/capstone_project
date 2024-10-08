from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model

# Get the default auth user model
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    '''
    Function: Allows users to register using their credentials
    '''
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(ObtainAuthToken):
    '''
    Function: Allows users to login using their credentials and obtain authentication token
    '''
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    '''
    Function: Allows users to view and update their profile
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user    # Ensures users can only update their own profile
    
class FollowUserView(generics.GenericAPIView):
    '''
    Function: Allows a user to follow another user,
    including error handling if the user to follow doesn't exist
    '''
    permission_classes = [IsAuthenticated]  # permissions

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)

            # Check if user to follow is legitimate 
            if user_to_follow != request.user and user_to_follow not in request.user.following.all():
                request.user.following.add(user_to_follow)
                serialized_user = UserSerializer(user_to_follow)
                return Response({
                    "detail": "Now following.",
                    "user": serialized_user.data
                    }, status=status.HTTP_201_CREATED)
            else:
                return Response({"Detail": "You cannot follow yourself or someone you're already following!"})
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UnfollowUserView(generics.GenericAPIView):
    '''
    Function: Allows a user to unfollow another user,
    including error handling if the user to unfollow doesn't exist
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            
            # Check if user to unfollow is legitimate
            if user_to_unfollow != request.user and user_to_unfollow in request.user.following.all():
                request.user.following.remove(user_to_unfollow)
                serialized_user = UserSerializer(user_to_unfollow)
                return Response({
                    "detail": "Unfollowed.",
                    "user": serialized_user.data
                    }, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"Detail": "You cannot unfollow yourself or a non-exitent follower!"})
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)