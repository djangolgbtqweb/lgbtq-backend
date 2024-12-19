from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)  # Optional bio field

    def __str__(self):
        return f"{self.user.username}'s Profile"


