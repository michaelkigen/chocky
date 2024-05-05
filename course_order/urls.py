from rest_framework.routers import DefaultRouter
from .views import Orders_course_view
from django.urls import path, include



urlpatterns = [
    path("order-course/", Orders_course_view.as_view()),
    ]