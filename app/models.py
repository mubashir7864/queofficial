from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Postform(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    #image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Optional ImageField
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title 