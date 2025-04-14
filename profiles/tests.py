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