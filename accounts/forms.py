from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Blog

# User Update Form (for updating user information)
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Profile Update Form (for updating profile information)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']

# Post Creation Form (for creating new posts)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'media_attachments', 'emoji']

# Comment Creation Form (for creating comments on posts)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'emoji', 'media_attachments']

# Blog Creation Form (for creating new blogs)
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']

