from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer
from .register import register_social_user
from .google import Google
from rest_framework.exceptions import AuthenticationFailed

class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_token = serializer.validated_data.get('auth_token')

        user_data = Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise AuthenticationFailed('Error validating token')

        if user_data['aud'] != "220876944567-b609gs9pbjrrjpaapm3mlvtft3hjhn45.apps.googleusercontent.com":
            raise AuthenticationFailed('Invalid token')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'  # Adjust the provider here as needed
        res = register_social_user(provider=provider, user_id=user_id, email=email, name=name)
        
        # Extract tokens
        refresh_token = res['tokens']['refresh_token']
        access_token = res['tokens']['access_token']

        # Save tokens in cookies
        response = Response({"message": "User authenticated successfully","access_token":str(access_token)})
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        
        return response
