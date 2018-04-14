from django import forms
from .models import *

class PostForm(forms.ModelForm):  # Для сайта
    class Meta:
        model = Post
        fields = ['title', 'text']