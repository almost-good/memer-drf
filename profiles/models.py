from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile model for user profiles.
    """

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


def create_profile(sender, instance, created, **kwargs):
    """
    Create a new profile for the user when they are created.
    """

    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
