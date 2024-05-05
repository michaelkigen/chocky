import cloudinary.uploader
from rest_framework import serializers
from .models import Course, Sub_Course , Photos
import cloudinary


class Sub_Course_serialier(serializers.ModelSerializer):
    class Meta:
        model = Sub_Course
        fields =[
            "sub_course_id","title","price","discount","study_method",
            "duration","qualification","more_info","picture","date"
        ]
        extra_kwargs = {'course_id': {'read_only': True}}
        
        def create(self,validated_data):
            images = validated_data.pop('picture', None)
            instance = super().create(validated_data)
            if images:
                upload_image = cloudinary.uploader.upload(images)
                instance.picture = upload_image['secure_url']
                instance.save()
            return instance
        
        
class Course_serialier(serializers.ModelSerializer):
    
    
    
    class Meta:
        model = Course
        fields =[
            "course_id","title","price","discount","study_method",
            "duration","qualification","more_info","picture","date"
        ]
        extra_kwargs = {'course_id': {'read_only': True}}
        
        def create(self,validated_data):
            images = validated_data.pop('picture', None)
            instance = super().create(validated_data)
            if images:
                upload_image = cloudinary.uploader.upload(images)
                instance.picture = upload_image['secure_url']
                instance.save()
            return instance
        
        
class Photos_serializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields =[
            "photo_id","couse","sub_course","picture"
        ]
        extra_kwargs = {'photo_id': {'read_only': True}}
        
        def create(self,validated_data):
            pic = validated_data.pop("picture", None)
            instance = super().create(validated_data)
            if pic:
                upload_image = cloudinary.uploader.upload(pic)
                instance.picture = upload_image['secure_url']
                instance.save()
            return instance