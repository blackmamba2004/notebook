from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.tokens import RefreshToken

from notes.models import Note
from users.models import User
from .permissions import IsAdminOrReadOnly, IsOwner
from .serializers import NoteDetailSerializer, UserSerializer

# class NoteAPIView(APIView):

#     def get(self, request):
#         notes = Note.objects.all()
#         return Response(
#             {
#                 'notes': NoteSerializer(notes, many=True).data
#             }
#         )
    
#     def post(self, request):
#         serializer = NoteSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 'note': serializer.data
#             }
#         )
    
#     def put(self, request, *args, **kwargs):

    
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response(
#                 {
#                     "error": "Method PUT is not allowed"
#                 }
#             )
        
#         try:
#             instance = Note.objects.get(pk=pk)
        
#         except:
#             return Response(
#                 {
#                     "error": "Object does not exist"
#                 }
#             )
        
#         serializer = NoteSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 "note": serializer.data
#             }
#         )
    
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')

#         if not pk:
#             return Response(
#                 {
#                     "error": "Method DELETE is not allowed"
#                 }
#             )
        
#         try:
#             note = Note.objects.get(pk=pk).delete()
        
#         except:
#             return Response(
#                 {
#                     "error": "Object does not exist"
#                 }
#             )

#         return Response(
#             {
#                 "note": "delete note" + str(pk)
#             }
#         )
    
#     def patch(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response(
#                 {
#                     "error": "Method PATCH is not allowed"
#                 }
#             )
        
#         try:
#             instance = Note.objects.get(pk=pk)

#         except:
#             return Response(
#                 {
#                     "error": "Object does not exist"
#                 }
#             )
        
#         serializer = NoteSerializer(data=request.data, instance=instance, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(
#             {
#                 "note": serializer.data
#             }
#         )


# class NoteAPIList(generics.ListCreateAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly, )


# class NoteAPIUpdate(generics.RetrieveUpdateAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#     # permission_classes = (IsOwnerOrReadOnly, )
#     permission_classes = (IsAuthenticated, )


# class NoteAPIDestroy(generics.RetrieveDestroyAPIView):
    # queryset = Note.objects.all()
    # serializer_class = NoteSerializer
    # permission_classes = (IsAdminOrReadOnly, )


# class NoteAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    
    # queryset = Note.objects.select_related('author').only(
    #     'id', 'title', 'content', 'author_id', 'author__first_name', 'author__last_name'
    # )

    def get_serializer(self, *args, **kwargs):
        return NoteDetailSerializer(*args, **kwargs)

    def get_queryset(self):
        if self.action != 'list':
            return Note.objects.select_related('author')\
                   .only('id', 'title', 'content', 'author_id', 
                         'author__first_name', 'author__last_name')
        return Note.objects.all()
    
    def get_permissions(self):
        action_permissions = {
            'retrieve': [IsOwner],
            'create': [IsAuthenticated],
            'update': [IsOwner],
            'partial_update': [IsOwner],
            'destroy': [IsOwner]
        }
        permission_classes = action_permissions.get(self.action, [IsAuthenticatedOrReadOnly])

        return [permission() for permission in permission_classes]

    @action(methods=['get'], detail=True, url_path='author')
    def author(self, request: Request, pk=None):
        note = self.get_object()
        user = note.author
        return Response({'author': UserSerializer(user).data})
    
    # @action(methods=['get'], detail=True, url_path='content')
    # def content(self, request: Request, pk=None):
    #     note = self.get_object()
        


# class CustomLoginView(APIView):
#     def post(self, request: Request, *args, **kwargs):
#         data= request.data

#         email = data.get('email', None)
#         password = data.get('password', None)

#         if email is None and password is None:
#             return Response(
#                 {
#                     'error': 'Нужны и логин, и пароль!'
#                 }, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         user = authenticate(email=email, password=password)

#         if user is None:
#             return Response(
#                 {
#                     'error': 'Неверные данные!'
#                 }, 
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
        
#         refresh = RefreshToken.for_user(user)

#         refresh.payload.update({
#             'user_id': user.id
#         })

#         return Response(
#             {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token)
#             }, 
#             status=status.HTTP_200_OK
#         )

