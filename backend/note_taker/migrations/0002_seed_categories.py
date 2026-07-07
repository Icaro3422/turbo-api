from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model('note_taker', 'Category')
    categories = [
        {"title": "Work", "color": "#3B82F6"},
        {"title": "Personal", "color": "#10B981"},
        {"title": "Ideas", "color": "#F59E0B"},
        {"title": "Archive", "color": "#6B7280"},
    ]
    for cat in categories:
        Category.objects.get_or_create(title=cat["title"], defaults={"color": cat["color"]})


def reverse_seed(apps, schema_editor):
    Category = apps.get_model('note_taker', 'Category')
    Category.objects.filter(title__in=["Work", "Personal", "Ideas", "Archive"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('note_taker', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_seed),
    ]
