from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    image=models.ImageField(upload_to="images")   
    
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.IntegerField()
    doctor=models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.user.email
    
class Book(models.Model):
    require = models.CharField(max_length=200,null=True)
    description = models.TextField()
    start_time = models.DateField()
    end_time = models.TimeField()