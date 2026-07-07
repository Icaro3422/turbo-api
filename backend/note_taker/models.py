from django.db import models
from django.conf import settings


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
