from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Sub_Course, Photos
from .serializers import Sub_Course_serialier, Course_serialier ,Photos_serializer

from cloudinary import api
from django.conf import settings


class Courses_APIview(APIView):
    def get(self,request):
        courses =Course.objects.all()
        serializer =  Course_serialier(courses, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = Course_serialier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_401_UNAUTHORIZED)

class CourseDetailed_view(APIView):
    def get_object(self,pk):
        try:
            return Course.objects.get(course_id = pk)
        except Course.DoesNotExist:
            return None
    
    def get(self,request,pk):
        course =self.get_object(pk)
        if course:
            course_serialier = Course_serialier(course)
            sub_course = Sub_Course.objects.filter(course=pk)
            sub_course_serializer = Sub_Course_serialier(sub_course, many = True)
            photo = Photos.objects.filter(couse= course)
            photo_serializer = Photos_serializer(photo, many=True)
            response = {
                "courses":course_serialier.data,
                "sub_courses":sub_course_serializer.data,
                "photos":photo_serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({"error":"course with the id not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request , pk):
        course =self.get_object(pk)
        
        if not course:
            return Response({"error":"course with the id not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Course_serialier(course,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,pk):
        course = self.get_object(pk)
        if course:
            course.delete()
            return Response(status=status.HTTP_200_OK)
        return Response( status=status.HTTP_404_NOT_FOUND)
    
# SUB COURSE

class Sub_courses_APIview(APIView):
   
    def post(self, request):
        serializer = Sub_Course_serialier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_401_UNAUTHORIZED)
    

class Sub_courseDetailed_view(APIView):
    def get_object(self,pk):
        try:
            return Sub_Course.objects.get(sub_course_id = pk)
        except Sub_Course.DoesNotExist:
            return None
    
    def get(self,request,pk):
        sub_course =self.get_object(pk)
        if sub_course:
            sub_course_serializer = Sub_Course_serialier(sub_course)
            photo = Photos.objects.filter(sub_course=sub_course)
            photo_serializer = Photos_serializer(photo, many=True)
            response = {
                "sub_courses":sub_course_serializer.data,
                "photos":photo_serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({"error":"sub course with the id not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request , pk):
        sub_course =self.get_object(pk)
        
        if not sub_course:
            return Response({"error":"sub course with the id not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Sub_Course_serialier(sub_course,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,pk):
        sub_course = self.get_object(pk)
        if sub_course:
            sub_course.delete()
            return Response(status=status.HTTP_200_OK)
        return Response( status=status.HTTP_404_NOT_FOUND)
    
# photos

class PhotoApivies(APIView):
    
    def post(self, request):
        serializer = Photos_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
class PhotoDetailedAPiview(APIView):
    def get_object(self,pk):
        try:
            return Photos.objects.get(photo_id = pk )
        except Photos.DoesNotExist:
            return None
        
    def get(self,pk):
        photo = self.get_object(pk)
        if photo:
            serializer = Photos_serializer(photo)
            return Response(serializer.data , status= status.HTTP_200_OK)
        return Response({"error":"not found"} , status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request ,pk):
        photo = self.get_object(pk)
        if not photo:
            return Response({"error":"not found"} , status=status.HTTP_404_NOT_FOUND)
        serializer = Photos_serializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status= status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_404_NOT_FOUND)
    
    
    def delete(self,pk):
        photo = self.get_object(pk)
        if photo:
            image = photo.picture
            try:
                api.delete_resources([image])
            except:
                print("didn't delete image from cloudinary")
            photo.delete()
            return Response(status=status.HTTP_200_OK)
        return Response({'error':'photo not found'},status=status.HTTP_404_NOT_FOUND)
                
        