from itertools import count
from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
    def test_can_list_posts(self):
        """
        Ensure we can list posts.
        """
        
        testuser = User.objects.get(username='testuser')
        Post.objects.create(
            owner=testuser,
            title='Test Post'
        )
        url = '/posts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logged_in_user_can_create_post(self):
        """
        Ensure logged in user can create a post.
        """
        
        self.client.login(username='testuser', password='testpassword')
        url = '/posts/'
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }
        response = self.client.post(url, data)
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_post(self):
        """
        Ensure logged out user cannot create a post.
        """
        
        url = '/posts/'
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)