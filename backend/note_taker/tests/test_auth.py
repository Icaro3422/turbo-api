from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AuthAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.refresh_url = '/api/auth/refresh/'

    def test_register_success(self):
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertIn('id', response.data)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_register_duplicate_email(self):
        User.objects.create_user(email='test@example.com', password='testpass123')
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_too_short(self):
        data = {'email': 'test@example.com', 'password': 'short'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        User.objects.create_user(email='test@example.com', password='testpass123')
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        User.objects.create_user(email='test@example.com', password='testpass123')
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        data = {'email': 'nonexistent@example.com', 'password': 'testpass123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        User.objects.create_user(email='test@example.com', password='testpass123')
        login_response = self.client.post(
            self.login_url,
            {'email': 'test@example.com', 'password': 'testpass123'}
        )
        refresh_token = login_response.data['refresh']
        response = self.client.post(self.refresh_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_invalid_token(self):
        response = self.client.post(
            self.refresh_url,
            {'refresh': 'invalid-token'}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
