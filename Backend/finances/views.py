from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .models import User
from .serializers import UserSerializer
import os

def get_tokens_for_user(user):
    refresh = RefreshToken()
    refresh['id'] = user.id
    refresh['email'] = user.email
    return {
        'token': str(refresh.access_token),
        'refresh': str(refresh),
    }

# Registro de usuario
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response(
                {'message': 'Todos los campos son obligatorios'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'message': 'El usuario ya existe'},
                status=status.HTTP_409_CONFLICT
            )

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        return Response(
            {'message': 'Usuario registrado exitosamente'},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {'message': 'Error al registrar el usuario'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Login de usuario
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'message': 'Todos los campos son obligatorios'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'message': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.password and user.provider == 'google':
            return Response(
                {'message': "Esta cuenta fue creada con Google. Usa 'Continuar con Google'."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {'message': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        tokens = get_tokens_for_user(user)
        return Response({
            'token': tokens['token'],
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        })
    except Exception as e:
        return Response(
            {'message': 'Error al iniciar sesión'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Login con Google
@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    try:
        google_token = request.data.get('token')

        idinfo = id_token.verify_oauth2_token(
            google_token,
            google_requests.Request(),
            os.environ.get('GOOGLE_CLIENT_ID')
        )

        email = idinfo['email']
        username = idinfo.get('name', email.split('@')[0])
        provider_id = idinfo['sub']

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'provider': 'google',
                'provider_id': provider_id,
            }
        )

        tokens = get_tokens_for_user(user)
        return Response({
            'token': tokens['token'],
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'isNewUser': created
        })
    except Exception as e:
        return Response(
            {'message': 'Error en autenticación con Google'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )