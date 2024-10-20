from rest_framework.authentication import get_authorization_header, BaseAuthentication
from authentication.models import User
from rest_framework import exceptions
import jwt
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except (InvalidToken, TokenError):
            raise AuthenticationFailed('Token is invalid or expired', code='token_not_valid')


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        
        if not auth_header:
            return None  # No authentication header was provided
        
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split()

        # Ensure that the token has the correct structure
        if len(auth_token) != 2 or auth_token[0].lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Token not valid')

        token = auth_token[1]

        try:
            # Decode the JWT token with the specified algorithm
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            username = payload.get('username')  # Safely get the username

            if username is None:
                raise exceptions.AuthenticationFailed('Token does not contain username')

            # Retrieve the user based on the username from the payload
            user = User.objects.get(username=username)

            return (user, token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token is expired, login again')

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Token is invalid')

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return None  # Return None if no authentication was possible
