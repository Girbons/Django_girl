from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'published_date')

class RegistrationForm(UserCreationForm):
    email = fields.EmailField()
    first_name = fields.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        first_name = self.cleaned_data['first_name']
        user.first_name = first_name
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'post', )
