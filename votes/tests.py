from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from posts.models import Post
from comments.models import Comment
from .models import Vote
from rest_framework import status
from rest_framework.test import APITestCase


class VoteListViewTests(APITestCase):
    def setUp(self):
        user_one = User.objects.create_user(
            username='testuser_one',
            password='testpassword'
        )
        user_two = User.objects.create_user(
            username='testuser_two',
            password='testpassword'
        )
        
        post = Post.objects.create(
            owner=user_one,
            title='Test Post owned by User One',
        )
        comment = Comment.objects.create(
            owner=user_one,
            post=post,
            content='Test Comment owned by User One',
        )
        
        post_ct = ContentType.objects.get_for_model(Post)
        Vote.objects.create(
            owner=user_one,
            content_type=post_ct,
            object_id=post.id, # type: ignore
            value=1
        )
        
    def test_can_list_votes(self):
        """
        Ensure votes are listed correctly.
        """
        
        url = '/votes/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)