from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from posts.models import Post
from votes.models import Vote


class Comment(models.Model):
    """
    Comment model to represent user comments on posts.
    """

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    vote = GenericRelation(Vote, related_query_name='post')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
