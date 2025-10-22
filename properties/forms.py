from django import forms
from .models import Property

class ScheduleVisitForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Your Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Your Email'
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Your Phone Number'
        })
    )
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-900',
            'type': 'date'
        })
    )
    preferred_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-900',
            'type': 'time'
        })
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Any specific requirements or questions...',
            'rows': 4
        })
    )


    from django import forms
from .models import ContactMessage  # optional model for storing messages

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage  # or use forms.Form if no model
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-3 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-3 border rounded'}),
            'subject': forms.TextInput(attrs={'class': 'w-full p-3 border rounded'}),
            'message': forms.Textarea(attrs={'class': 'w-full p-3 border rounded', 'rows': 5}),
        }
