from django.db import models
import uuid

class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images')
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='brand_images')
    
    def __str__(self):
        return self.name
    
class Functionalities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='functinalities_images')
    
    def __str__(self):
        return self.name
    
class Kits(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='kits_images')
    
    def __str__(self):
        return self.name
    
class Tools(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='tool_images', null=True)
    description = models.TextField(null=True)
    
    category = models.ForeignKey(Categories, on_delete=models.CASCADE , related_name="tools",null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE , related_name="tools",null=True)
    functionalities = models.ForeignKey(Functionalities, on_delete=models.CASCADE  ,related_name="tools",null=True)
    kits = models.ForeignKey(Kits, on_delete=models.CASCADE , related_name="tools",null=True)
    
    def __str__(self):
        return self.name
    
class ToolImages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='tool_images')
    tool = models.ForeignKey(Tools, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tool.name



