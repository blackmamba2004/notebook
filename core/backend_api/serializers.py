from django.contrib.auth import get_user_model
from rest_framework import serializers
from notes.models import Note

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('full_name',)
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class NoteDetailSerializer(serializers.ModelSerializer):
    # author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_full_name = serializers.SerializerMethodField()
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'author_full_name']

    def get_author_full_name(self, obj):
        return obj.author.get_full_name()
  

# class NoteSerializer(serializers.ModelSerializer):
#     author = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     class Meta:
#         model = Note
#         fields = ['id', 'title', 'content', 'author']