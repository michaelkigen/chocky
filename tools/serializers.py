from rest_framework import serializers
from .models import Categories, Brand, Functionalities, Kits, Tools, ToolImages
import cloudinary
from cloudinary.models import CloudinaryField

from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name', 'description', 'image']
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        instance = super().create(validated_data)
        if image:
            # Upload image to Cloudinary
            cloudinary_storage_config = settings.CLOUDINARY_STORAGE
            cloudinary.config(
                cloud_name=cloudinary_storage_config['CLOUD_NAME'],
                api_key=cloudinary_storage_config['API_KEY'],
                api_secret=cloudinary_storage_config['API_SECRET']
            )
            uploaded_image = cloudinary.uploader.upload(image)
            instance.image = uploaded_image['secure_url']
            instance.save()
        return instance


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'image']
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        instance = super().create(validated_data)
        if image:
            # Upload image to Cloudinary
            cloudinary_storage_config = settings.CLOUDINARY_STORAGE
            cloudinary.config(
                cloud_name=cloudinary_storage_config['CLOUD_NAME'],
                api_key=cloudinary_storage_config['API_KEY'],
                api_secret=cloudinary_storage_config['API_SECRET']
            )
            uploaded_image = cloudinary.uploader.upload(image)
            instance.image = uploaded_image['secure_url']
            instance.save()
        return instance


class FunctionalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Functionalities
        fields = ['id', 'name', 'description', 'image']
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        instance = super().create(validated_data)
        if image:
            # Upload image to Cloudinary
            cloudinary_storage_config = settings.CLOUDINARY_STORAGE
            cloudinary.config(
                cloud_name=cloudinary_storage_config['CLOUD_NAME'],
                api_key=cloudinary_storage_config['API_KEY'],
                api_secret=cloudinary_storage_config['API_SECRET']
            )
            uploaded_image = cloudinary.uploader.upload(image)
            instance.image = uploaded_image['secure_url']
            instance.save()
        return instance


class KitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kits
        fields = ['id', 'name', 'description', 'image']
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        instance = super().create(validated_data)
        if image:
            # Upload image to Cloudinary
            cloudinary_storage_config = settings.CLOUDINARY_STORAGE
            cloudinary.config(
                cloud_name=cloudinary_storage_config['CLOUD_NAME'],
                api_key=cloudinary_storage_config['API_KEY'],
                api_secret=cloudinary_storage_config['API_SECRET']
            )
            uploaded_image = cloudinary.uploader.upload(image)
            instance.image = uploaded_image['secure_url']
            instance.save()
        return instance




class ToolSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = Tools
        fields = [
                 'id', 'name', 'price', 'image', 'description',
                  'category', 'brand', 'functionalities', 'kits'
                  ]
        extra_kwargs = {'id': {'read_only': True}}
        
    def create(self, validated_data):
        image_data = validated_data.pop('image')
        tool = Tools.objects.create(**validated_data)
        cloudinary_storage_config = settings.CLOUDINARY_STORAGE
        cloudinary.config(
            cloud_name=cloudinary_storage_config['CLOUD_NAME'],
            api_key=cloudinary_storage_config['API_KEY'],
            api_secret=cloudinary_storage_config['API_SECRET']
        )
        tool.image = cloudinary.uploader.upload(image_data)['url']
        tool.save()
        return tool


class ToolImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToolImages
        exclude = ('id',"image","tool")
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        image_data = validated_data.pop('image')
        tool = Tools.objects.create(**validated_data)
        cloudinary_storage_config = settings.CLOUDINARY_STORAGE
        cloudinary.config(
            cloud_name=cloudinary_storage_config['CLOUD_NAME'],
            api_key=cloudinary_storage_config['API_KEY'],
            api_secret=cloudinary_storage_config['API_SECRET']
        )
        tool.image = cloudinary.uploader.upload(image_data)['url']
        tool.save()
        return tool

