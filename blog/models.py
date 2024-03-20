from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    summary=models.CharField(max_length=255,blank=True)
    image=models.ImageField(upload_to='blogimage',default=None)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    draft=models.BooleanField(default=False)
    author=models.CharField(max_length=255,default=False)
    
    def __str__(self):
        return self.title
    
    