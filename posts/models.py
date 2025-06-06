from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from votes.models import Vote


class Post(models.Model):
    """
    Post model for user posts.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='images/', default='../troll-face_fdpdrn', blank=True
    )
    vote = GenericRelation(Vote, related_query_name='post')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.owner} - {self.title}'  # type: ignore
