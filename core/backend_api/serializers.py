from django.contrib.auth import get_user_model
from rest_framework import serializers
from notes.models import Note

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('email',)
        fields = ('first_name', 'last_name', 'email')


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Note
        fields = '__all__'
