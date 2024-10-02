from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from . import serializers
from rest_framework.exceptions import ValidationError
import re
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer,CustomTokenObtainPairSerializer,BlogPostSerializer,UserProfileUpdateSerializer
from .models import BlogPost
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to the Blog API!")

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        if not self.is_password_strong(password):
            raise ValidationError("Password does not meet the minimum strength criteria.")
        serializer.save(password=make_password(password))

    def is_password_strong(self, password):
        # Check minimum length
        if len(password) < 8:
            return False
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False
        
        # Check for at least one digit
        if not re.search(r'\d', password):
            return False
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        
        return True

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


#if user is logged in show the object of the user
class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

#if user is logged in update the object of the user
class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user


# Only logged users can create the post
class CreateBlogPostView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the author as the current logged-in user
        serializer.save(author=self.request.user)

# List all the posts for every users
class ListBlogPostView(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

# Get a single post details
class SingleBlogPostView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

class UpdateBlogPostView(generics.UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_update(self, serializer):
        post = self.get_object()
        # Check if the user is the author of the post
        if post.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this post.")
        serializer.save()

# Only logged users can delete their profile
class DeleteBlogPostView(generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        # Check if the user is the author of the post
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this post.")
        instance.delete()
