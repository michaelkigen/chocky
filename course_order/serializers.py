from rest_framework import serializers
from .models import Orderd_course
from tools.serializers import ToolSerializer
from courses.models import Course

class Orderd_couse_serializer(serializers.ModelSerializer):
    class Meta:
        model = Orderd_course
        fields = ["id","phone","created_at", "courses", "user"]
        
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'user': {'read_only': True},
        }
