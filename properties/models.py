from django.conf import settings
from django.db import models

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from agents.models import Agent

from django.db import models
from django.utils import timezone

class ScheduledVisit(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='scheduled_visits')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.property.title} ({self.preferred_date} {self.preferred_time})"


class PropertyType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Property Type"
        verbose_name_plural = "Property Types"
        ordering = ['name']

    def __str__(self):
        return self.name


class Property(models.Model):

    
    @property
    def image_url(self):
        """Return the URL of the primary image or a default image if none exists."""
        primary = self.images.filter(is_primary=True).first()
        if primary and primary.image:
            return primary.image.url
        return 'https://via.placeholder.com/300x200?text=No+Image'
    # 🔹 Define all choices first
    STATUS_CHOICES = [
        ('for_sale', 'For Sale'),
        ('for_rent', 'For Rent'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
    ]

    TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('house', 'House'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
        ('office', 'Office'),
        ('shop', 'Shop'),
    ]

    FURNISHING_CHOICES = [
        ('furnished', 'Fully Furnished'),
        ('semi_furnished', 'Semi Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]

    # 🔹 Now you can safely use them below
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_id = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='for_sale')

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    custom_type = models.ForeignKey(
        PropertyType, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Optional: select a custom property type (overrides default type)"
    )
    
    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_id = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='for_sale')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Location
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100, default='Nagpur')
    state = models.CharField(max_length=100, default='Maharashtra')
    pincode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_description = models.TextField(blank=True)
    
    # Property Details
    total_area = models.DecimalField(max_digits=8, decimal_places=2, help_text="Area in square feet")
    built_up_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    bedrooms = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    bathrooms = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    balconies = models.PositiveIntegerField(default=0)
    garage = models.PositiveIntegerField(default=0)
    floors = models.PositiveIntegerField(default=1)
    floor_number = models.PositiveIntegerField(default=1, help_text="For apartments")
    year_built = models.PositiveIntegerField()
    furnishing = models.CharField(max_length=20, choices=FURNISHING_CHOICES, default='unfurnished')
    
    # Additional Features
    featured = models.BooleanField(default=False)
    featured_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Relationships
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='properties')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-featured', '-created_at']
    
    def __str__(self):
        return f"{self.property_id} - {self.title}"
    
    @property
    def primary_image_url(self):
        primary = self.images.filter(is_primary=True).first()
        if primary and primary.image:
            return primary.image.url
        return 'https://via.placeholder.com/600x400?text=No+Image'

    @property
    def gallery_images(self):
        """Return all images ordered by `order` field or any logic."""
        return self.images.all().order_by('order')
    
    
    
    @property
    def is_featured(self):
        if self.featured_until:
            return self.featured and timezone.now() <= self.featured_until
        return self.featured
    
    def save(self, *args, **kwargs):
        if not self.property_id:
            # Generate property ID: PROP-YYMM-XXXX
            from datetime import datetime
            from django.utils.crypto import get_random_string
            date_part = datetime.now().strftime('%y%m')
            random_part = get_random_string(4, '0123456789')
            self.property_id = f"PROP-{date_part}-{random_part}"
        super().save(*args, **kwargs)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['is_primary', 'order']
    
    def __str__(self):
        return f"Image for {self.property.title}"

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, default='fas fa-check')
    category = models.CharField(max_length=50, default='general')
    
    def __str__(self):
        return self.name

class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='amenities')
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Property amenities"
        unique_together = ['property', 'amenity']
    
    def __str__(self):
        return f"{self.property.title} - {self.amenity.name}"

class NearbyPlace(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='nearby_places')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    distance = models.CharField(max_length=50, help_text="e.g., 1.2 km, 15 min walk")
    icon_class = models.CharField(max_length=50, default='fas fa-map-marker-alt')
    
    def __str__(self):
        return f"{self.name} near {self.property.title}"

# models.py
from django.db import models

class PropertyView(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    # New fields for IP geolocation
    country = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    isp = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.property.title} viewed from {self.ip_address}"


from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class SavedProperty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="property_saved_properties")
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name="saved_by")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} saved {self.property.title}"
