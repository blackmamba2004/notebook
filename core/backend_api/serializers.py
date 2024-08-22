from django.contrib.auth import get_user_model
from rest_framework import serializers
from notes.models import Note

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class NoteDetailSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'author']

class NoteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

