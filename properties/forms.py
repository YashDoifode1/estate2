from django import forms
from .models import Property, PropertyImage, NearbyPlace

# Add this ContactForm class to your existing forms.py
class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Your Full Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Your Email Address'
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Your Phone Number (Optional)'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Subject'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Your Message',
            'rows': 5
        })
    )


class PropertyFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('all', 'All Status'),
        ('for_sale', 'For Sale'),
        ('for_rent', 'For Rent'),
    ]
    
    TYPE_CHOICES = [
        ('all', 'All Types'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('house', 'House'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
    ]
    
    PRICE_RANGES = [
        ('all', 'Any Price'),
        ('0-20', 'Under ₹20 Lakhs'),
        ('20-40', '₹20-40 Lakhs'),
        ('40-60', '₹40-60 Lakhs'),
        ('60-100', '₹60 Lakhs - ₹1 Crore'),
        ('100-999', 'Above ₹1 Crore'),
    ]
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, initial='all')
    property_type = forms.ChoiceField(choices=TYPE_CHOICES, required=False, initial='all')
    location = forms.CharField(required=False)
    bedrooms = forms.ChoiceField(choices=[('all', 'Any')] + [(str(i), str(i)) for i in range(1, 6)], required=False, initial='all')
    price_range = forms.ChoiceField(choices=PRICE_RANGES, required=False, initial='all')
    search = forms.CharField(required=False)

class ScheduleVisitForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Your Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Your Email'
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Your Phone Number'
        })
    )
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-900',
            'type': 'date',
            'placeholder': 'Preferred Date'
        })
    )
    preferred_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-900',
            'type': 'time',
            'placeholder': 'Preferred Time'
        })
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-900',
            'placeholder': 'Additional Message (Optional)',
            'rows': 4
        })
    )