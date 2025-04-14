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
    
    def test_user_can_update_own_post(self):
        """
        Ensure user can update their own post.
        """
        
        self.client.login(username='testuser_one', password='testpassword')
        url = '/posts/1/'
        data = {
            'title': 'Updated User One Post',
        }
        response = self.client.put(url, data)
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'Updated User One Post') # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_user_post(self):
        """
        Ensure user can't update another user's post.
        """
        
        self.client.login(username='testuser_one', password='testpassword')
        url = '/posts/2/'
        data = {
            'title': 'User One updates User Two Post',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_post(self):
        """
        Ensure user can delete their own post.
        """
        
        self.client.login(username='testuser_one', password='testpassword')
        url = '/posts/1/'
        response = self.client.delete(url)
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_user_cant_delete_another_user_post(self):
        """
        Ensure user can't delete another user's post.
        """
        
        self.client.login(username='testuser_one', password='testpassword')
        url = '/posts/2/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)