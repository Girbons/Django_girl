from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Permission)
# Register your models here.
