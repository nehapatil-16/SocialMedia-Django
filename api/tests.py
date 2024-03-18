from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_register_view(self):
        data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'testpassword',
        }
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Registration data received and pending approval')

    def test_login_view(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post('/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertTrue('userid' in response.data)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_profile_view(self):
        response = self.client.get('/user-profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_post_view(self):
        response = self.client.get('/user-post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_friend_request_view(self):
        response = self.client.get('/friend-request/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_friendship_view(self):
        response = self.client.get('/friendship/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_report_request_view(self):
        response = self.client.get('/report-request/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_create_view(self):
        data = {
            'user': self.user.id,
            'user_post': 1,  # Assuming there's a user post with ID 1 in the database
            'content': 'Test comment content',
        }
        response = self.client.post('/comment-create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_comments_view(self):
        response = self.client.get('/get-comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

