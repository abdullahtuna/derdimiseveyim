from django import forms
from .models import Post, Comment, Contact

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'