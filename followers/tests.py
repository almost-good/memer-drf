from django.contrib.auth.models import User
import test
from .models import Follower
from rest_framework import status
from rest_framework.test import APITestCase


class FollowerListViewTests(APITestCase):
    def setUp(self):
        self.testuser_one = User.objects.create_user(
            username='testuser_one',
            password='testpassword'
        )
        self.testuser_two = User.objects.create_user(
            username='testuser_two',
            password='testpassword'
        )

    def test_can_list_followers(self):
        """
        Ensure followers are listed correctly.
        """
        
        Follower.objects.create(
            owner=self.testuser_one,
            followed=self.testuser_two
        )
        url = '/followers/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logged_in_user_can_follow_another_user(self):
        """
        Ensure logged in user can follow another user.
        """
        
        self.client.login(username='testuser_one', password='testpassword')
        url = '/followers/'
        data = {
            'followed': self.testuser_two.id # type: ignore
        }
        response = self.client.post(url, data)
        count = Follower.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_logged_out_user_cannot_follow_another_user(self):
        """
        Ensure logged out user cannot follow another user.
        """
        
        url = '/followers/'
        data = {
            'followed': self.testuser_two.id # type: ignore
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
class FollowerDetailViewTests(APITestCase):
    def setUp(self):
        self.testuser_one = User.objects.create_user(
            username='testuser_one',
            password='testpassword'
        )
        self.testuser_two = User.objects.create_user(
            username='testuser_two',
            password='testpassword'
        )
        
        Follower.objects.create(
            owner=self.testuser_one,
            followed=self.testuser_two
        )
        
    def test_can_retrieve_follower_using_valid_id(self):
        """
        Ensure follower can be retrieved using a valid ID.
        """
        
        url = '/followers/1/'
        response = self.client.get(url)
        self.assertEqual(response.data['followed'], self.testuser_two.id) # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_cant_retrieve_follower_using_invalid_id(self):
        """
        Ensure follower cannot be retrieved using an invalid ID.
        """
        
        url = '/followers/999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_user_can_unfollow(self):
        """
        Ensure logged in user can unfollow another user.
        """
        
        self.client.login(username='testuser_one', password='testpassword')
        url = '/followers/1/'
        response = self.client.delete(url)
        count = Follower.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)