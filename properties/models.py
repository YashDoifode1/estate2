from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
import uuid

User = get_user_model()

class PropertyType(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, default='fas fa-home')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, default='fas fa-check')
    
    def __str__(self):
        return self.name

class Property(models.Model):
    PROPERTY_STATUS = [
        ('for_sale', 'For Sale'),
        ('for_rent', 'For Rent'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
    ]
    
    FURNISHING_CHOICES = [
        ('furnished', 'Fully Furnished'),
        ('semi_furnished', 'Semi Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    
    # Basic Information
    property_id = models.CharField(max_length=20, unique=True, default=uuid.uuid4().hex[:8].upper())
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PROPERTY_STATUS, default='for_sale')
    
    # Location
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100, default='Nagpur')
    state = models.CharField(max_length=100, default='Maharashtra')
    pincode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_description = models.TextField(blank=True)
    
    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_display = models.CharField(max_length=100)  # Formatted price like "₹75 Lakhs"
    price_per_sqft = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Property Details
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    total_area = models.DecimalField(max_digits=8, decimal_places=2)  # in sq.ft.
    built_up_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    carpet_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    year_built = models.PositiveIntegerField(null=True, blank=True)
    floor = models.PositiveIntegerField(default=1)
    total_floors = models.PositiveIntegerField(default=1)
    furnishing = models.CharField(max_length=20, choices=FURNISHING_CHOICES, default='unfurnished')
    garage = models.PositiveIntegerField(default=0)
    
    # Features
    amenities = models.ManyToManyField(Amenity, blank=True)
    featured = models.BooleanField(default=False)
    available_from = models.DateField(null=True, blank=True)
    
    # Agent Information
    agent = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.property_id}")
        
        # Format price display
        if self.price >= 10000000:  # 1 Crore
            self.price_display = f"₹{self.price/10000000:.2f} Crore"
        elif self.price >= 100000:  # 1 Lakh
            self.price_display = f"₹{self.price/100000:.1f} Lakhs"
        else:
            self.price_display = f"₹{self.price:,.0f}"
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.property_id}"
    
    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'pk': self.pk, 'slug': self.slug})

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-is_primary']
    
    def __str__(self):
        return f"Image for {self.property.title}"

class NearbyPlace(models.Model):
    property = models.ForeignKey(Property, related_name='nearby_places', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    distance = models.CharField(max_length=50)  # e.g., "1.2 km", "500 m"
    icon_class = models.CharField(max_length=50, default='fas fa-map-marker-alt')
    
    def __str__(self):
        return f"{self.name} near {self.property.title}"

class PropertyView(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']

class FavoriteProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'property']
        ordering = ['-added_at']