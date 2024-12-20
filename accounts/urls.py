from django.urls import path
from .views import RegisterView, LoginView, PasswordResetView, ChangePasswordView, CommentListCreateView, BlogCreateView, BlogListView, BlogDetailView, LikeToggleView, PostListCreateView, PostDetailView, profile_view, ProfileUpdateView, CommentDeleteView, PostDeleteView, BlogDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),  # Profile update view
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_id>/like/', LikeToggleView.as_view(), name='like_toggle'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('posts/<int:post_id>/comments/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('posts/<int:post_id>/delete/', PostDeleteView.as_view(), name='post_delete'),
]




