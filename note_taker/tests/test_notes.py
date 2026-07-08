from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from note_taker.models import Category, Note

User = get_user_model()


class NoteAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.other_user = User.objects.create_user(email='other@example.com', password='testpass123')
        self.category = Category.objects.create(title="Work", color="#3B82F6")
        self.other_category = Category.objects.create(title="Personal", color="#10B981")
        self.note = Note.objects.create(
            title="Test Note",
            description="Test description",
            category=self.category,
            user=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_note(self):
        data = {
            'title': 'New Note',
            'description': 'New description',
            'category_id': self.category.id
        }
        response = self.client.post('/api/notes/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Note')
        self.assertEqual(response.data['description'], 'New description')
        self.assertIn('last_update', response.data)

    def test_list_notes(self):
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_notes_only_user_notes(self):
        Note.objects.create(
            title="Other User Note",
            category=self.category,
            user=self.other_user
        )
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Note')

    def test_retrieve_note(self):
        response = self.client.get(f'/api/notes/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Note')
        self.assertEqual(response.data['description'], 'Test description')
        self.assertIn('category', response.data)

    def test_update_note(self):
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'category_id': self.other_category.id
        }
        response = self.client.put(f'/api/notes/{self.note.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        self.assertEqual(response.data['description'], 'Updated description')
        self.assertEqual(response.data['category']['id'], self.other_category.id)

    def test_delete_note(self):
        response = self.client.delete(f'/api/notes/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_filter_by_category(self):
        Note.objects.create(
            title="Personal Note",
            category=self.other_category,
            user=self.user
        )
        response = self.client.get(f'/api/notes/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Note')

    def test_ordering_by_last_update(self):
        note2 = Note.objects.create(
            title="Note 2",
            category=self.category,
            user=self.user
        )
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Note 2')

    def test_cannot_access_other_user_note(self):
        other_note = Note.objects.create(
            title="Other Note",
            category=self.category,
            user=self.other_user
        )
        response = self.client.get(f'/api/notes/{other_note.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
