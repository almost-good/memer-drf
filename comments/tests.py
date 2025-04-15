from django.contrib.auth.models import User
from posts.models import Post
from .models import Comment
from rest_framework import status
from rest_framework.test import APITestCase


class CommentListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='testuser_postowner',
            password='testpassword'
        )
        User.objects.create_user(
            username='testuser_commenter',
            password='testpassword'
        )
        Post.objects.create(
            owner=User.objects.get(username='testuser_postowner'),
            title='Test Post'
        )
        
    def test_can_list_comments(self):
        """
        Ensure comments are listed correctly.
        """
        
        url = '/comments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logged_in_user_can_create_comment(self):
        """
        Ensure logged in user can create a comment.
        """
        
        self.client.login(
            username='testuser_commenter', 
            password='testpassword'
        )
        postowner = User.objects.get(username='testuser_postowner')
        post = Post.objects.get(owner=postowner)
        url = '/comments/'
        data = {
            'content': 'This is a test comment.',
            'post': post.id # type: ignore
        }
        response = self.client.post(url, data)
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_logged_out_user_cannot_create_comments(self):
        """
        Ensure logged out user cannot create a comments.
        """
        
        url = '/comments/'
        data = {
            'content': 'This is a test comment.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)