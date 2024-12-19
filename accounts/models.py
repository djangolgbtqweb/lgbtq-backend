from django.contrib.auth.models import User
from django.db import models

# Profile model: Stores extra information about the user, such as profile picture and bio.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # One-to-one relationship with User.
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)  # Profile picture field.
    bio = models.TextField(null=True, blank=True)  # Optional bio field to store user information.

    def __str__(self):
        return f"{self.user.username}'s Profile"  # Display the user's profile in a readable format.

# Post model: Stores individual posts, created by users.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  # Foreign key to the User model.
    title = models.CharField(max_length=200)  # Title of the post.
    content = models.TextField()  # Content of the post.
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the post was created.
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the post was last updated.
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # Optional image for the post.
    media_attachments = models.JSONField(null=True, blank=True)  # Store media URLs (images, videos, audio) in JSON format.
    emoji = models.TextField(null=True, blank=True)  # Store emoji used in the post.

    def __str__(self):
        return self.title  # Return the post title when displaying the post.

# Comment model: Stores comments made by users on posts.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  # Foreign key to the User model.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  # Foreign key to the Post model.
    content = models.TextField()  # Content of the comment.
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the comment was created.
    emoji = models.TextField(null=True, blank=True)  # Store emoji used in the comment.
    media_attachments = models.JSONField(null=True, blank=True)  # Store media URLs (images, videos, audio) in JSON format.

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"  # Display comment's user and post title.

# Like model: Stores likes made by users on posts.
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")  # Foreign key to the User model.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")  # Foreign key to the Post model.
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the like was created.

    class Meta:
        unique_together = ('user', 'post')  # Ensure a user can only like a post once.
    
    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"  # Display like's user and post title.

# Emoji model: Store emojis used in posts and comments.
class Emoji(models.Model):
    name = models.CharField(max_length=50)  # Name of the emoji.
    symbol = models.CharField(max_length=10)  # The actual emoji character or shortcode.
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the emoji was created.

    def __str__(self):
        return self.symbol  # Display the emoji's symbol.




