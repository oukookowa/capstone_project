from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom user model icluding extra fields for more user details
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='accounts/profile_photos/', default='accounts/profile_photos/default_photo.png', blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    cover_photo = models.ImageField(upload_to='accounts/cover_photos/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.username
    