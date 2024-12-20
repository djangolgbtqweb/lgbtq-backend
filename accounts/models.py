from django.contrib.auth.models import User
from django.db import models

# Profile model: Stores extra information about the user, such as profile picture and bio.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Blog model: Stores blog posts with a payment status for posting.
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)  # Field to track payment status
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title

# Post model: Stores individual posts, created by users.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    media_attachments = models.JSONField(null=True, blank=True)
    emoji = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

# Comment model: Stores comments made by users on posts.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    emoji = models.TextField(null=True, blank=True)
    media_attachments = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

# Like model: Stores likes made by users on posts.
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"

# Emoji model: Store emojis used in posts and comments.
class Emoji(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbol





