from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category, Note

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    note_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'color', 'note_count']

    def get_note_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.notes.filter(user=request.user).count()
        return 0


class NoteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'last_update', 'category', 'category_id']
        read_only_fields = ['id', 'last_update']
