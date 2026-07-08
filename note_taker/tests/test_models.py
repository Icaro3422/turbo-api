from django.test import TestCase
from django.contrib.auth import get_user_model
from note_taker.models import Category, Note


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(title="Test", color="#FF0000")
        self.assertEqual(category.title, "Test")
        self.assertEqual(category.color, "#FF0000")
        self.assertEqual(str(category), "Test")

    def test_category_verbose_name_plural(self):
        self.assertEqual(Category._meta.verbose_name_plural, "categories")


class NoteModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.category = Category.objects.create(title="Work", color="#3B82F6")

    def test_note_creation(self):
        note = Note.objects.create(
            title="Test Note",
            description="Test description",
            category=self.category,
            user=self.user
        )
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.description, "Test description")
        self.assertEqual(str(note), "Test Note")
        self.assertEqual(note.category, self.category)
        self.assertEqual(note.user, self.user)

    def test_note_ordering(self):
        note1 = Note.objects.create(title="Note 1", category=self.category, user=self.user)
        note2 = Note.objects.create(title="Note 2", category=self.category, user=self.user)
        notes = list(Note.objects.all())
        self.assertEqual(notes[0], note2)
        self.assertEqual(notes[1], note1)

    def test_note_category_relationship(self):
        note = Note.objects.create(title="Test", category=self.category, user=self.user)
        self.assertEqual(self.category.notes.count(), 1)
        self.assertIn(note, self.category.notes.all())

    def test_note_user_relationship(self):
        note = Note.objects.create(title="Test", category=self.category, user=self.user)
        self.assertEqual(self.user.notes.count(), 1)
        self.assertIn(note, self.user.notes.all())

    def test_note_cascade_delete_category(self):
        category_id = self.category.id
        self.category.delete()
        self.assertFalse(Note.objects.filter(category_id=category_id).exists())

    def test_note_cascade_delete_user(self):
        user_id = self.user.id
        self.user.delete()
        self.assertFalse(Note.objects.filter(user_id=user_id).exists())
