from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os

from order.token_auth import JWTAuthentication

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ['http', 'https']



class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        response_data = {
            "user": serializer.data,
            "access_token": access_token,
        }
        response = Response(response_data, status=status.HTTP_201_CREATED)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        return response




class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the user data from serializer
        user_data = serializer.data
        email = user_data['email']

        # Retrieve the user object
        user = User.objects.get(email=email)
        user.is_verified = True
        # Generate tokens
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        # Set cookies
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.set_cookie(key='refresh_token', value=str(refresh_token), httponly=True)

        return response

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    authentication_classes = [JWTAuthentication]

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # Deserialize the request data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Extract the refresh token from the request cookies
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                # Blacklist the refresh token
                RefreshToken(refresh_token).blacklist()
                
                # Create a response with a success message
                response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
                
                # Clear the refresh token cookie
                response.delete_cookie('refresh_token')
                
                # Clear the access token cookie as well
                response.delete_cookie('access_token')
                
                return response
            except TokenError:
                # Handle token error
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle case when refresh token is not found in cookies
            return Response({'error': 'Refresh token not found'}, status=status.HTTP_400_BAD_REQUEST)
