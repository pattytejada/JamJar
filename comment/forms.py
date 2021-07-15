from django import forms
from comment.models import Comment

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import Profile

class CommentForm(forms.ModelForm):
    body = forms.CharField()

    class Meta:
        model = Comment
        fields = ['body']