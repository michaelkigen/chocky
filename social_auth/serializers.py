from rest_framework import serializers
from .google import Google
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed



class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    