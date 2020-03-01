from django.forms import ModelForm
from .models import Post, Group
from django import forms

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("group", "text")
        labels = {"group": "Выберите категорию", "text": "Текст поста"}
        widgets = {"text": forms.Textarea, 
        }
        
