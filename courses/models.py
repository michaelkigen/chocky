from django.db import models
import uuid
# Create your models here.

MODE_OF_STUDY = (
    ('ONLINE','online'),
    ('PHYSICAL','physical')
)

class Course(models.Model):
    course_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    discount = models.DecimalField(max_digits=4,decimal_places=2,null=True)
    study_method = models.CharField(max_length=50,choices=MODE_OF_STUDY, default="online")
    duration = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    more_info = models.TextField()
    picture = models.FileField(upload_to='courses', null=True)
    date = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.title
    
class Sub_Course(models.Model):
    sub_course_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name="sub_course")
    title = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    discount = models.DecimalField(max_digits=4,decimal_places=2,null=True)
    study_method = models.CharField(max_length=50,choices=MODE_OF_STUDY, default="online")
    duration = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    more_info = models.TextField()
    picture = models.FileField(upload_to='sub_courses', null=True)
    date = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"{self.course} {self.title}"
    
class Photos(models.Model):
    photo_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    couse = models.ForeignKey(Course, verbose_name=("pics"), on_delete=models.CASCADE,null=True)
    sub_course =models.ForeignKey(Sub_Course, verbose_name=("pics"), on_delete=models.CASCADE,null=True)
    picture = models.FileField(upload_to='all_courses', null=True)
    
    def __str__(self):
        return f"{self.couse}  {self.sub_course}"