from django.contrib.auth.models import User
from django.db import models
from django.http import request
from django.utils import timezone


# Create your models here.



class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(default=timezone.now, blank=True, null=False)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post)
