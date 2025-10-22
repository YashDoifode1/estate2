from django import forms
from .models import BlogComment, BlogNewsletterSubscriber

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-900',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-900',
                'placeholder': 'Your Email'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-900',
                'placeholder': 'Your Comment',
                'rows': 4
            }),
        }

class BlogNewsletterForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-yellow-500',
            'placeholder': 'Enter your email address'
        })
    )
    
    class Meta:
        model = BlogNewsletterSubscriber
        fields = ['email']