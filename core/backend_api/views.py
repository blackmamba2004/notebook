from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import detail
from notes.models import Note
from .serializers import NoteSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework import generics, viewsets
from users.models import User


class NoteAPIView(APIView):

    def get(self, request):
        notes = Note.objects.all()
        return Response(
            {
                'notes': NoteSerializer(notes, many=True).data
            }
        )
    
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'note': serializer.data
            }
        )
    
    def put(self, request, *args, **kwargs):

    
        pk = kwargs.get("pk", None)
        if not pk:
            return Response(
                {
                    "error": "Method PUT is not allowed"
                }
            )
        
        try:
            instance = Note.objects.get(pk=pk)
        
        except:
            return Response(
                {
                    "error": "Object does not exist"
                }
            )
        
        serializer = NoteSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "note": serializer.data
            }
        )
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        if not pk:
            return Response(
                {
                    "error": "Method DELETE is not allowed"
                }
            )
        
        try:
            note = Note.objects.get(pk=pk).delete()
        
        except:
            return Response(
                {
                    "error": "Object does not exist"
                }
            )

        return Response(
            {
                "note": "delete note" + str(pk)
            }
        )
    
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response(
                {
                    "error": "Method PATCH is not allowed"
                }
            )
        
        try:
            instance = Note.objects.get(pk=pk)

        except:
            return Response(
                {
                    "error": "Object does not exist"
                }
            )
        
        serializer = NoteSerializer(data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "note": serializer.data
            }
        )


class NoteAPIList(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class NoteAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    # permission_classes = (IsOwnerOrReadOnly, )
    permission_classes = (IsAuthenticated, )


class NoteAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAdminOrReadOnly, )


# class NoteAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    
    queryset = Note.objects.select_related('author').all()
    serializer_class = NoteSerializer
    
    def get_permissions(self):
        
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrReadOnly]
        
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]

        return [permission() for permission in permission_classes]

    @action(methods=['get'], detail=True, url_path='author', permission_classes=IsOwnerOrReadOnly)
    def author(self, request: HttpRequest, pk=None):
        note = self.get_object()
        user = note.author
        return Response({'author': UserSerializer(user).data})
    
