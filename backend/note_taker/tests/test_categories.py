from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from note_taker.models import Category, Note

User = get_user_model()


class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.other_user = User.objects.create_user(email='other@example.com', password='testpass123')
        self.category = Category.objects.create(title="Work", color="#3B82F6")

    def test_list_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_categories_includes_note_count(self):
        Note.objects.create(title="Note 1", category=self.category, user=self.user)
        Note.objects.create(title="Note 2", category=self.category, user=self.user)
        Note.objects.create(title="Note 3", category=self.category, user=self.other_user)

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/categories/')

        work_category = next(c for c in response.data['results'] if c['title'] == 'Work')
        self.assertEqual(work_category['note_count'], 2)

    def test_retrieve_single_category(self):
        response = self.client.get(f'/api/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Work')
        self.assertEqual(response.data['color'], '#3B82F6')
        self.assertIn('note_count', response.data)

    def test_retrieve_nonexistent_category(self):
        response = self.client.get('/api/categories/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_categories_read_only(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/categories/', {'title': 'New', 'color': '#000000'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(
            f'/api/categories/{self.category.id}/',
            {'title': 'Updated', 'color': '#000000'}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(f'/api/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_categories_public_no_auth_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
