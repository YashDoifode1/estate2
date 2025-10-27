from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    newsletter_subscription = models.BooleanField(default=False)
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


def profile_picture_upload_path(instance, filename):
    return f"profile_pictures/user_{instance.user.id}/{filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)  # <-- this updates automatically on save

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Force timestamp update if profile picture changed
        if self.pk:
            old = UserProfile.objects.get(pk=self.pk)
            if old.profile_picture != self.profile_picture:
                self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class UserPreferences(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preferences')
    interest_buying = models.BooleanField(default=True)
    interest_renting = models.BooleanField(default=False)
    interest_selling = models.BooleanField(default=False)
    interest_commercial = models.BooleanField(default=False)
    min_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    preferred_locations = models.JSONField(default=list, blank=True)
    property_types = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} Preferences"

class NotificationSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='notification_settings')
    email_property_recommendations = models.BooleanField(default=True)
    email_price_drop_alerts = models.BooleanField(default=True)
    email_new_listings = models.BooleanField(default=True)
    email_market_updates = models.BooleanField(default=True)
    email_promotional_offers = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} Notification Settings"

class PrivacySettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='privacy_settings')
    data_sharing = models.BooleanField(default=False)
    personalized_ads = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} Privacy Settings"

class LoginSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='login_sessions')
    device = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    session_key = models.CharField(max_length=40, blank=True, null=True)
    last_active = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.device}"

class SavedProperty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="account_saved_properties")
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'property']

class Consultation(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    MODE_CHOICES = [
        ('video_call', 'Video Call'),
        ('phone_call', 'Phone Call'),
        ('in_person', 'In Person'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='consultations')
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='agent_consultations')
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    end_time = models.TimeField()
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='video_call')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    TYPE_CHOICES = [
        ('price_drop', 'Price Drop'),
        ('consultation_reminder', 'Consultation Reminder'),
        ('property_match', 'Property Match'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"


