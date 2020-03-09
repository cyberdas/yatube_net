from django.forms import ModelForm
from .models import Post, Group, Comment
from django import forms

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("group", "text", "image")
        labels = {"group": "Выберите категорию", "text": "Текст поста", "image": "Изображение"}
        widgets = {"text": forms.Textarea, 
        }
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text", )
        labels = {"text": "Текст комментария"}
        widgets = {"text": forms.Textarea}
