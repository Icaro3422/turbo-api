from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class Category(models.Model):
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=7)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="notes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    class Meta:
        ordering = ['-last_update']

    def __str__(self):
        return self.title


PREDEFINED_CATEGORIES = [
    {"title": "Random Thoughts", "color": "#EF9C66"},
    {"title": "School", "color": "#FCDC94"},
    {"title": "Personal", "color": "#78ABA8"},
]


def seed_categories(apps, schema_editor):
    for cat in PREDEFINED_CATEGORIES:
        Category.objects.get_or_create(title=cat["title"], defaults={"color": cat["color"]})
