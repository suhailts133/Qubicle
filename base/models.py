# models.py
from django.db import models
from django.utils import timezone

class Image(models.Model):
    image = models.ImageField(upload_to='uploaded_images/', unique=False)
    # New field indicating if it's the last image

    def __str__(self):
        return self.image.name


class JSONFile(models.Model):
    file = models.FileField(upload_to='uploaded_json/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    

class JSONModelQP(models.Model):
    file = models.FileField(upload_to='uploaded_QP/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

