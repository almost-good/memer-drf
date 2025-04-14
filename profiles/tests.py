from django.contrib.auth.models import User
from .models import Profile
from rest_framework import status
from rest_framework.test import APITestCase


class ProfileListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
    def test_can_list_profiles(self):
        """
        Ensure profiles are listed correctly.
        """
        
        url = '/profiles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileDetailViewTests(APITestCase):
    def setUp(self):
        testuser_one = User.objects.create_user(
            username='testuser_one',
            password='testpassword'
        )
        testuser_two = User.objects.create_user(
            username='testuser_two',
            password='testpassword'
        )
        
        Profile.objects.filter(
            owner=testuser_one
        ).update(
            flair='User One Flair'
        )
        Profile.objects.filter(
            owner=testuser_two
        ).update(
            flair='User Two Flair'
        )
        
    def test_can_retrieve_profile_using_valid_id(self):
        """
        Ensure profile can be retrieved using a valid ID.
        """
        
        url = '/profiles/1/'
        response = self.client.get(url)
        self.assertEqual(response.data['flair'], 'User One Flair') # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_cant_retrieve_profile_using_invalid_id(self):
        """
        Ensure profile can't be retrieved using a invalid ID.
        """
        
        url = '/profiles/999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)