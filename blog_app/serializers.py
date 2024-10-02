from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import BlogPost,BlogTag

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile','password','profile_picture']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile', 'profile_picture']  # Include 'profile_picture' if you have this field

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        
        # If you have a profile picture field, update it
        if 'profile_picture' in validated_data:
            instance.profile_picture = validated_data['profile_picture']
        instance.save()
        return instance
    
class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        # Override the validate method to include custom behavior if needed
        data = super().validate(attrs)
        data.update({
            'username': self.user.username,
            'user_id': self.user.id  # Add user ID here
        })
        return data

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ['id', 'name']

class BlogPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSummarySerializer(read_only=True)
    image_base64 = serializers.CharField(write_only=True, allow_null=True, required=False)
    image = serializers.CharField(read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'tags', 'author', 'created_at', 'image_base64', 'image']  # Include 'image' in the fields
        read_only_fields = ['author', 'created_at', 'image']  # Make 'image' read-only

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        image_base64 = validated_data.pop('image_base64', None)  # Handle the base64 image

        # Create the blog post
        post = BlogPost.objects.create(**validated_data)

        if image_base64:
            # Store the base64 string in the 'image' field (you may want to decode and save as a file instead)
            post.image = image_base64
            post.save()

        # Handle tags
        for tag_data in tags_data:
            tag, created = BlogTag.objects.get_or_create(name=tag_data['name'])
            post.tags.add(tag)

        return post