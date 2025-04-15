from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from posts.models import Post
from comments.models import Comment
from .models import Vote
from rest_framework import status
from rest_framework.test import APITestCase


class VoteListViewTests(APITestCase):
    def setUp(self):
        self.user_one = User.objects.create_user(
            username='testuser_one',
            password='testpassword'
        )
        user_two = User.objects.create_user(
            username='testuser_two',
            password='testpassword'
        )
        
        self.post = Post.objects.create(
            owner=self.user_one,
            title='Test Post owned by User One',
        )
        self.post_ct = ContentType.objects.get_for_model(Post)
        
        self.comment = Comment.objects.create(
            owner=self.user_one,
            post=self.post,
            content='Test Comment owned by User One',
        )
        self.comment_ct = ContentType.objects.get_for_model(Comment)
        
    def test_can_list_votes(self):
        """
        Ensure votes are listed correctly.
        """
        
        url = '/votes/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_vote_on_post(self):
        """
        Ensure logged in user can vote on a post.
        """
        
        self.client.login(username='testuser_two', password='testpassword')
        
        url = '/votes/'
        data = {
            'content_type': self.post_ct.id, # type: ignore
            'object_id': self.post.id, # type: ignore
            'value': 1
        }
        
        response = self.client.post(url, data)
        count = Vote.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_in_user_can_vote_on_comment(self):
        """
        Ensure logged in user can vote on a comment.
        """
        
        self.client.login(username='testuser_two', password='testpassword')
        
        url = '/votes/'
        data = {
            'content_type': self.comment_ct.id, # type: ignore
            'object_id': self.comment.id, # type: ignore
            'value': 1
        }
        
        response = self.client.post(url, data)
        count = Vote.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_vote(self):
        """
        Ensure logged out user cannot create a vote.
        """
        
        url = '/votes/'
        data = {
            'content_type': self.post_ct.id, # type: ignore
            'object_id': self.post.id, # type: ignore
            'value': 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)