from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import BlogPost, BlogTag
import base64
from django.core.files.base import ContentFile
from django.utils.html import escape 
import os

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_picture_as_base64 = serializers.SerializerMethodField()  # To return base64 string in response

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'password', 'profile_picture', 'profile_picture_as_base64']

    def get_profile_picture_as_base64(self, obj):
        """Convert the profile picture to base64 string for the response."""
        if obj.profile_picture:
            try:
                # Open the image file
                with open(obj.profile_picture.path, 'rb') as image_file:
                    # Encode the image in base64
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    ext = os.path.splitext(obj.profile_picture.name)[-1].replace('.', '')
                    return f"data:image/{ext};base64,{encoded_string}"
            except Exception as e:
                return None
        return None


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_picture_base64 = serializers.CharField(write_only=True, allow_null=True, required=False)  # Input base64 string
    profile_picture = serializers.ImageField(read_only=True)  # URL of the profile picture
    profile_picture_as_base64 = serializers.SerializerMethodField()  # To return base64 string in response

    class Meta:
        model = User
        fields = ['username', 'email', 'mobile', 'profile_picture', 'profile_picture_base64', 'profile_picture_as_base64']

    def get_profile_picture_as_base64(self, obj):
        """Convert the profile picture to base64 string for the response."""
        if obj.profile_picture:
            try:
                # Open the image file
                with open(obj.profile_picture.path, 'rb') as image_file:
                    # Encode the image in base64
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    ext = os.path.splitext(obj.profile_picture.name)[-1].replace('.', '')  # Get the image extension
                    return f"data:image/{ext};base64,{encoded_string}"
            except Exception as e:
                return None
        return None

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.mobile = validated_data.get('mobile', instance.mobile)

        # Handle profile picture update from base64 string
        profile_picture_base64 = validated_data.pop('profile_picture_base64', None)
        if profile_picture_base64:
            try:
                format, imgstr = profile_picture_base64.split(';base64,')
                ext = format.split('/')[-1]  # Extract the file extension (e.g., jpg, png)
                instance.profile_picture = ContentFile(base64.b64decode(imgstr), name=f"{instance.username}_profile.{ext}")
            except Exception as e:
                raise serializers.ValidationError("Invalid image data for profile picture.")

        instance.save()
        return instance
    
class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'username': self.user.username,
            'user_id': self.user.id
        })
        return data

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ['id', 'name']

class BlogPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    author = UserSummarySerializer(read_only=True)
    image_base64 = serializers.CharField(write_only=True, allow_null=True, required=False)  
    image = serializers.ImageField(read_only=True) 
    image_base64_read = serializers.SerializerMethodField()  

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'tags', 'author', 'created_at', 'image_base64', 'image', 'image_base64_read']
        read_only_fields = ['author', 'created_at', 'image', 'image_base64_read']

    def get_image_base64_read(self, obj):
        """This method returns the base64 string of the image for read operations."""
        if obj.image:
            try:
                with open(obj.image.path, 'rb') as image_file:
                    return base64.b64encode(image_file.read()).decode('utf-8')
            except Exception as e:
                return None
        return None

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        image_base64 = validated_data.pop('image_base64', None)

        # Create the blog post
        post = BlogPost.objects.create(**validated_data)
        
        # Handle images
        if image_base64:
            try:
                format, imgstr = image_base64.split(';base64,')
                ext = format.split('/')[-1]
                post.image = ContentFile(base64.b64decode(imgstr), name=f"{escape(post.title)}.{ext}")
                post.save()
            except Exception as e:
                raise serializers.ValidationError("Invalid image data")

        # Handle tags
        for tag_data in tags_data:
            tag, created = BlogTag.objects.get_or_create(name=tag_data['name'])
            post.tags.add(tag)

        return post
