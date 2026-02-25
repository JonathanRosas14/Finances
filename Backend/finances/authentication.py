from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from .models import User


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication for our custom User model.
    """
    
    def get_validated_token(self, raw_token):
        """
        Validate the JWT token.
        """
        try:
            validated_token = super().get_validated_token(raw_token)
            return validated_token
        except InvalidToken:
            raise AuthenticationFailed('Invalid token')
        except Exception as e:
            raise AuthenticationFailed(str(e))
    
    def get_user(self, validated_token):
        """
        Get the user from the validated token.
        """
        try:
            user_id = validated_token.get('user_id')
            if not user_id:
                user_id = validated_token.get('id')
            
            if not user_id:
                raise AuthenticationFailed('Token contains no user_id')
            
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        except Exception as e:
            raise AuthenticationFailed(str(e))
