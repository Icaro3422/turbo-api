from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model('note_taker', 'Category')
    categories = [
        {"title": "Random Thoughts", "color": "#EF9C66"},
        {"title": "School", "color": "#FCDC94"},
        {"title": "Personal", "color": "#78ABA8"},
    ]
    for cat in categories:
        Category.objects.get_or_create(title=cat["title"], defaults={"color": cat["color"]})


def reverse_seed(apps, schema_editor):
    Category = apps.get_model('note_taker', 'Category')
    Category.objects.filter(title__in=["Random Thoughts", "School", "Personal"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('note_taker', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_seed),
    ]
