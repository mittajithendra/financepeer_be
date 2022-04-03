from pyexpat import model
from turtle import title
from django.db import models
from django.contrib.auth.models import AbstractUser

class Blog(models.Model):
    eid = models.IntegerField()
    bid = models.IntegerField()
    title = models.TextField()
    content = models.TextField()

class User(AbstractUser):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)

    REQUIRED_FIELDS=[]