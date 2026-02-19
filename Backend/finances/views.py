from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .models import User
import bcrypt
import os
from .models import User, Category
from .serializers import CategorySerializer
from rest_framework_simplejwt.tokens import AccessToken


def get_tokens_for_user(user):
    refresh = RefreshToken()
    refresh['id'] = user.id
    refresh['email'] = user.email
    return {
        'token': str(refresh.access_token),
        'refresh': str(refresh),
    }


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

        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user = User(username=username, email=email, password=hashed)
        user.save()

        return Response(
            {'message': 'Usuario registrado exitosamente'},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        print(f"Error en register: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


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

        if not bcrypt.checkpw(
            password.encode('utf-8'),
            user.password.encode('utf-8')
        ):
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
        print(f"Error en login: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


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
        print(f"Error en google_auth: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Obtener categorías del usuario
@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response(
                {'message': 'Token no proporcionado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        
        user = User.objects.get(id=user_id)
        categories = Category.objects.filter(user=user).order_by('-created_at')
        serializer = CategorySerializer(categories, many=True)
        
        return Response(serializer.data)
    except Exception as e:
        print(f"Error en get_categories: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Crear categoría
@api_view(['POST'])
@permission_classes([AllowAny])
def create_category(request):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response(
                {'message': 'Token no proporcionado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)
        
        request.user = user
        serializer = CategorySerializer(data=request.data, context={'request': request})
        
        if not serializer.is_valid():
            errors = serializer.errors
            first_error = next(iter(errors.values()))[0]
            return Response(
                {'message': str(first_error)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        category = serializer.save(user=user)
        
        return Response({
            'message': 'Categoría creada exitosamente',
            'category': CategorySerializer(category).data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Error en create_category: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Actualizar categoría
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_category(request, category_id):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response(
                {'message': 'Token no proporcionado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)
        
        try:
            category = Category.objects.get(id=category_id, user=user)
        except Category.DoesNotExist:
            return Response(
                {'message': 'Categoría no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        request.user = user
        serializer = CategorySerializer(category, data=request.data, context={'request': request})
        
        if not serializer.is_valid():
            errors = serializer.errors
            first_error = next(iter(errors.values()))[0]
            return Response(
                {'message': str(first_error)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        
        return Response({'message': 'Categoría actualizada exitosamente'})
        
    except Exception as e:
        print(f"Error en update_category: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Eliminar categoría
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_category(request, category_id):
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response(
                {'message': 'Token no proporcionado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['id']
        user = User.objects.get(id=user_id)
        
        try:
            category = Category.objects.get(id=category_id, user=user)
        except Category.DoesNotExist:
            return Response(
                {'message': 'Categoría no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        category.delete()
        
        return Response({'message': 'Categoría eliminada exitosamente'})
        
    except Exception as e:
        print(f"Error en delete_category: {e}")
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )