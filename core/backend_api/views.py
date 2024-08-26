from datetime import datetime, timedelta
import jwt
from core.settings import SECRET_KEY
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.models import Note
from .permissions import IsOwner
from .serializers import (NoteListSerializer, NoteDetailSerializer, 
                          UserSerializer, EmailSerializer,
                          RegistrationSerializer)

User = get_user_model()

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
    
    def get_permissions(self):
        print(f"Вызов {self.get_permissions.__name__}")
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


class Mailer(GenericAPIView):
    serializer_class = EmailSerializer
    MESSAGE = 'Привет, если вы не получали это письмо, то проигнорируйте его.'
    SENDER = 'a@gmail.com'
    MAIN_LINK = 'http://127.0.0.1:8000/api/v1/'

    def post(self, request: Request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            to_this_email = serializer.validated_data['email']

            uuid = urlsafe_base64_encode(force_bytes(to_this_email))

            token = jwt.encode({
                'email': to_this_email,
                'exp': datetime.now() + timedelta(minutes=10)
            }, key=SECRET_KEY, algorithm='HS256')

            send_mail('Registration', f'{self.MESSAGE}\n{self.MAIN_LINK}{uuid}/{token}/', 
                      self.SENDER, [to_this_email])

            return Response(
                {
                    'message': f'Было отправлено письмо на указанный адрес: {to_this_email}'
                },
                status=status.HTTP_200_OK
            )
        
        return Response(
            {
                'error': 'Ошибка, почта невалидна!'
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )


class ConfirmEmailAPI(GenericAPIView):

    def get(self, request: Request, *args, **kwargs):
        uuid = kwargs.get('uuid')

        token = kwargs.get('token')
        try:
            email = force_str(urlsafe_base64_decode(uuid))

            if default_token_generator.check_token(email, token):
                return Response(
                    {
                        'message': f'Письмо прочитано!, {email}'
                    }
                )
            else:
                return Response(
                    {
                        'error': 'Срок действия токена'
                    }
                )

        except DjangoUnicodeDecodeError:
            return Response(
                {
                    'error': 'Ошибка в декодировании ссылки!'
                }
            )


# class RegistrationAPI(GenericAPIView):

#     serializer_class = RegistrationSerializer
#     def post(self, request: Request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             password = data.pop('password')
#             User.objects.create_user(
#                 username = data['username'],
#                 email = data['email'], 
#                 password=password
#             )
            
