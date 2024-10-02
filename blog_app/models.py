from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=20, null=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

# Model to create Blog Tage
class BlogTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
# Model to create Blog Post
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(BlogTag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title