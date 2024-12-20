from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Profile, Post, Comment, Like, Emoji, Blog

# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def create(self, validated_data):
        # Prevent duplicate emails or usernames
        if User.objects.filter(email=validated_data['email']).count() >= 2:
            raise serializers.ValidationError("Email is already used twice.")
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError("Username is already taken.")

        # Create and return the user
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Serializer for user login
class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username_or_email = data['username_or_email']
        password = data['password']

        # Allow login with either username or email
        user = authenticate(username=username_or_email, password=password) or \
               authenticate(username=User.objects.filter(email=username_or_email).first(), password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        return user


# Serializer for changing user password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# Serializer for the Profile model
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'bio']


# Serializer for the Post model
class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the user's username instead of the ID.
    media_attachments = serializers.ListField(child=serializers.URLField(), required=False)
    emoji = serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'image', 'media_attachments', 'emoji']


# Serializer for the Comment model
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the user's username instead of the ID.
    post = serializers.StringRelatedField()  # Display the post's title instead of the ID.
    media_attachments = serializers.ListField(child=serializers.URLField(), required=False)
    emoji = serializers.CharField(required=False)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at', 'media_attachments', 'emoji']


# Serializer for the Like model
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the user's username instead of the ID.
    post = serializers.StringRelatedField()  # Display the post's title instead of the ID.

    class Meta:
        model = Like
        fields = ['user', 'post', 'created_at']


# Serializer for the Emoji model
class EmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoji
        fields = ['id', 'name', 'symbol', 'created_at']


# Serializer for the Blog model (with payment functionality)
class BlogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the user's username
    paid = serializers.BooleanField(default=False)  # To check if the blog was paid for

    class Meta:
        model = Blog
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'paid', 'image']

    def create(self, validated_data):
        # You can enforce that a blog can only be created after payment
        if not validated_data.get('paid', False):
            raise serializers.ValidationError("You must pay $10 to post a blog.")

        blog = Blog.objects.create(**validated_data)
        return blog
