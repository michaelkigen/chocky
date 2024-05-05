from django.urls import path, include
from .views import Courses_APIview, CourseDetailed_view,PhotoApivies,PhotoDetailedAPiview ,Sub_courses_APIview ,Sub_courseDetailed_view

urlpatterns = [
    path("course", Courses_APIview.as_view()),
    path('course/<uuid:pk>', CourseDetailed_view.as_view()),
    path("sub_course", Sub_courses_APIview.as_view()),
    path('sub_course/<uuid:pk>', Sub_courseDetailed_view.as_view()),
    path("photos", PhotoApivies.as_view()),
    path('course/<uuid:pk>', PhotoDetailedAPiview.as_view()),
    ]