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
            'post': post.id  # type: ignore
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


class CommentDetailViewTests(APITestCase):
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
        Comment.objects.create(
            owner=testuser_one,
            post=Post.objects.get(owner=testuser_one),
            content='User One Comment'
        )

    def test_can_retrieve_comment_using_valid_id(self):
        """
        Ensure comment can be retrieved using a valid ID.
        """

        url = '/comments/1/'
        response = self.client.get(url)
        self.assertEqual(
            response.data['content'], 'User One Comment'  # type: ignore
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_comment_using_invalid_id(self):
        """
        Ensure comment can't be retrieved using a invalid ID.
        """

        url = '/comments/999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_comment(self):
        """
        Ensure user can update their own comment.
        """

        self.client.login(username='testuser_one', password='testpassword')
        url = '/comments/1/'
        data = {
            'content': 'Updated Own Comment',
        }
        response = self.client.put(url, data)
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(
            comment.content, 'Updated Own Comment'  # type: ignore
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_user_comment(self):
        """
        Ensure user can't update another user's comment.
        """

        self.client.login(username='testuser_two', password='testpassword')
        url = '/comments/1/'
        data = {
            'content': 'User Two updates User One Comment',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_comment(self):
        """
        Ensure user can delete their own comment.
        """

        self.client.login(username='testuser_one', password='testpassword')
        url = '/comments/1/'
        response = self.client.delete(url)
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_another_user_comment(self):
        """
        Ensure user can't delete another user's comment.
        """

        self.client.login(username='testuser_two', password='testpassword')
        url = '/comments/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)