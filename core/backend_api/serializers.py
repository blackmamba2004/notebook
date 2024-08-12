from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, json
from users.models import User
from notes.models import Note
import io
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


# class NoteModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content


# class NoteSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()

# class NoteSerializer(serializers.Serializer):
    
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#     author_id = serializers.IntegerField()
#     created = serializers.DateTimeField(read_only=True)
#     updated = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         return Note.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.content = validated_data.get('content', instance.content)
#         instance.author = validated_data.get('author', instance.author)
#         instance.updated = validated_data.get('updated', instance.updated)
#         instance.save()
#         return instance
    

class NoteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Note
        fields = '__all__'
        # fields = ('id', 'title', 'content', 'author', 'created', 'updated')
    
