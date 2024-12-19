from django.urls import path
from .views import RegisterView, LoginView, PasswordResetView, ChangePasswordView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Register endpoint
    path('login/', LoginView.as_view(), name='login'),  # Login endpoint
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),  # Change password endpoint
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),  # Password reset endpoint
    path('profile/', views.profile_view, name='profile'),
    path('posts/', views.PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/comments/', views.CommentCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_id>/like/', views.LikeToggleView.as_view(), name='like_toggle'),
]

