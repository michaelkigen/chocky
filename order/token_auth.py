import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from authentication.models import User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the refresh token from the request cookies
        refresh_token = request.COOKIES.get('refresh_token')
        print("refresh token ",refresh_token)

        if refresh_token:
            try:
                # Decode the refresh token
                refresh_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])

                # Extract user information from the refresh token payload
                user_id = refresh_payload['user_id']
                # Retrieve the user object using the user_id
                user = User.objects.get(id=user_id)

                # You may also need to perform additional checks or validations here
                print(user)
                # Return the authenticated user and token
                return (user, None)
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Refresh token has expired')
            except jwt.InvalidTokenError:
                raise AuthenticationFailed('Invalid refresh token')
        else:
            raise AuthenticationFailed('Refresh token not provided')
