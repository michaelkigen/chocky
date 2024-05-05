from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from authentication.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
import random

def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)
    
from django.http import JsonResponse

def register_social_user(provider, user_id, email, name):
    try:
        # Check if user with provided email exists
        user = User.objects.get(email=email)

        # If user exists, authenticate and return tokens
        if user.auth_provider == provider:
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }
            return {'user': user.username, 'email': user.email, 'tokens': tokens}
        else:
            raise AuthenticationFailed(
                detail=f'Please continue your login using {user.auth_provider}'
            )
    except User.DoesNotExist:
        # Generate a random password for new users
        password = User.objects.make_random_password()

        # Create a new user
        user = User.objects.create_user(
            username=generate_username(name),
            email=email,
            password=make_password(password)
        )

        # Mark user as verified
        user.is_verified = True

        # Set authentication provider
        user.auth_provider = provider

        # Save the user
        user.save()

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }

        return {'user': user.username, 'email': user.email, 'tokens': tokens}

    except Exception as e:
        # Handle any other exceptions
        raise AuthenticationFailed(detail=str(e))
