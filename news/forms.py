from django import forms
from .models import Post


class NewsForm(forms.ModelForm):
    description = forms.CharField(min_length=15)

    class Meta:
        model = Post
        fields = ['title', 'author', 'description', 'text']


class ArticlesForm(forms.ModelForm):
    description = forms.CharField(min_length=15)

    class Meta:
        model = Post
        fields = ['title', 'author', 'description', 'text']