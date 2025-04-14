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
        Ensure posts are listed correctly.
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


class PostDetailViewTests(APITestCase):
    def setUp(self):
        testuser_one = User.objects.create_user(
            username='testuser_one',
            password='testpassword'
        )
        testuser_two = User.objects.create_user(
            username='testuser_two',
            password='testpassword'
        )
        Post.objects.create(
            owner=testuser_one,
            title='User One Post'
        )
        Post.objects.create(
            owner=testuser_two,
            title='User Two Post'
        )
        
    def test_can_retrieve_post_using_valid_id(self):
        """
        Ensure post can be retrieved using a valid ID.
        """
        
        url = '/posts/1/'
        response = self.client.get(url)
        self.assertEqual(response.data['title'], 'User One Post') # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_can_retrieve_post_using_invalid_id(self):
        """
        Ensure post can be retrieved using a valid ID.
        """
        
        url = '/posts/999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)