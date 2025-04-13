from email.mime import image
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flair = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to='images/', default='../troll-face_fdpdrn'
    )
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.owner}'s profile"