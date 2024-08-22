from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from notes.models import Note
from users.models import User
from .permissions import IsOwner
from .serializers import NoteListSerializer, NoteDetailSerializer, UserSerializer


class NoteViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        print(f"Вызов {self.get_serializer_class.__name__}")
        if self.action == 'list':
            return NoteListSerializer
        return NoteDetailSerializer

    def get_queryset(self):
        print(f"Вызов {self.get_queryset.__name__}")
        if self.action != 'list':
            return Note.objects.select_related('author')\
                   .only('id', 'title', 'content', 'author_id', 
                         'author__username')
        return Note.objects.all()
    
    # def get_permissions(self):
    #     print(f"Вызов {self.get_permissions.__name__}")
    #     action_permissions = {
    #         'retrieve': [IsOwner],
    #         'create': [IsAuthenticated],
    #         'update': [IsOwner],
    #         'partial_update': [IsOwner],
    #         'destroy': [IsOwner]
    #     }
    #     permission_classes = action_permissions.get(self.action, [IsAuthenticatedOrReadOnly])

    #     return [permission() for permission in permission_classes]

    @action(methods=['get'], detail=True, url_path='author')
    def author(self, request: Request, pk=None):
        note = self.get_object()
        user = note.author
        return Response({'author': UserSerializer(user).data})

