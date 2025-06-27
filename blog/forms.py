from django import forms
from .models import Comment, ContactMessage, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'subject': forms.TextInput(attrs={'class': 'form-input'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'featured_image', 'category', 'status', 'meta_title', 'meta_description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.TextInput(attrs={'class': 'form-textarea', 'rows': 10}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-multiselect'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
