from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Todo(models.Model):
    num = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    desc = models.CharField(max_length=1000)   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.CharField(max_length=100)
    
      
    def __str__(self):
        return self.title
    
    
class Contact(models.Model):
    num = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    datetime = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    desc = models.TextField()

    
    def __str__(self):
        return self.name


    
    
    
   