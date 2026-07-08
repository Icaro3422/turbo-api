from django.contrib import admin
from .models import Category, Note


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'color')
    search_fields = ('title',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'last_update')
    list_filter = ('category', 'user')
    search_fields = ('title', 'description')
