from django.db import models
from courses.models import Course
import uuid
from django.conf import settings


class Orderd_course(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='orderd_course') 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    
    def __str__(self):
        return f"Cart ID: {self.courses}, User: {self.user.username}"
