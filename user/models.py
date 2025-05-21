from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    status = models.CharField(max_length=100,blank=True)
    problems = models.CharField(max_length=100,blank=True)
    exercises = models.CharField(max_length=1000,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='image')
    image = models.ImageField(upload_to='photos/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.user.username} - {self.id}'