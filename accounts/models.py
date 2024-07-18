from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)  # User starts inactive
    activation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, default='I did not write a bio yet')
    birth_date = models.DateField(null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg')

    instagram_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    other_url = models.URLField(blank=True, null=True)
    link_image = models.ImageField(upload_to='links', default='links/personal_profile.png')

    def __str__(self) -> str:
        return self.user.username
    