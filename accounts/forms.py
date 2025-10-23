from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, UserProfile, UserPreferences, NotificationSettings, PrivacySettings

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter your email address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter your password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
        })
    )

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter your last name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter your email address'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter your phone number'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Create a password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Confirm your password'
        })
    )
    terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
        })
    )
    newsletter = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'terms', 'newsletter')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.newsletter_subscription = self.cleaned_data['newsletter']
        user.terms_accepted = self.cleaned_data['terms']
        
        if commit:
            user.save()
            # Create related profiles
            UserProfile.objects.create(user=user)
            UserPreferences.objects.create(user=user)
            NotificationSettings.objects.create(user=user)
            PrivacySettings.objects.create(user=user)
        return user

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter your last name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter your email address'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'location', 'bio']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
                'placeholder': 'Enter your phone number'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
                'placeholder': 'Enter your location'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
                'placeholder': 'Tell us about yourself',
                'rows': 4
            }),
        }

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter current password'
        })
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Confirm new password'
        })
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Current password is incorrect.')
        return current_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        
        validate_password(password2, self.user)
        return password2

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = [
            'interest_buying', 'interest_renting', 'interest_selling', 'interest_commercial',
            'min_budget', 'max_budget', 'preferred_locations', 'property_types'
        ]
        widgets = {
            'min_budget': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
                'placeholder': 'Minimum budget'
            }),
            'max_budget': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
                'placeholder': 'Maximum budget'
            }),
            'interest_buying': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
            'interest_renting': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
            'interest_selling': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
            'interest_commercial': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
        }

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = NotificationSettings
        fields = [
            'email_property_recommendations', 'email_price_drop_alerts', 
            'email_new_listings', 'email_market_updates', 'email_promotional_offers',
            'push_notifications', 'sms_notifications'
        ]
        widgets = {
            'email_property_recommendations': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
            'email_price_drop_alerts': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
            'email_new_listings': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
            'email_market_updates': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
            'email_promotional_offers': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
            'push_notifications': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
            'sms_notifications': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
        }

class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = PrivacySettings
        fields = ['data_sharing', 'personalized_ads']
        widgets = {
            'data_sharing': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
            'personalized_ads': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-900 bg-gray-100 border-gray-300 rounded focus:ring-blue-900'
            }),
        }

class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter your password to confirm'
        })
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('Invalid password.')
        return password

class NewsletterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-transparent',
            'placeholder': 'Enter your email address'
        })
    )