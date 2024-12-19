from django.urls import path
from .views import RegisterView, LoginView, PasswordResetView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Register endpoint
    path('login/', LoginView.as_view(), name='login'),  # Login endpoint
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),  # Change password endpoint
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),  # Password reset endpoint
]

