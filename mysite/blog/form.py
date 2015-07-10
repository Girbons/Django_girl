__author__ = 'alessandro'
from django import forms
from .models import Post
from django.utils import timezone

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'published_date')

