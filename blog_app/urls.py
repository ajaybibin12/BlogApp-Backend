from django.urls import path
from .views import SignupView, CustomLoginView,CreateBlogPostView,ListBlogPostView,SingleBlogPostView,UpdateBlogPostView,DeleteBlogPostView,UserProfileUpdateView,UserProfileView
from rest_framework_simplejwt.authentication import JWTAuthentication

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/',UserProfileUpdateView.as_view(), name='profile'),
    path('posts/create/', CreateBlogPostView.as_view(), name='create-post'),
    path('posts/', ListBlogPostView.as_view(), name='list-posts'),
    path('posts/<int:id>/', SingleBlogPostView.as_view(), name='single-post'),
    path('posts/<int:id>/update/', UpdateBlogPostView.as_view(), name='update-post'),
    path('posts/<int:id>/delete/', DeleteBlogPostView.as_view(), name='post-delete'),
]