from django.db import models
from django.core.validators import MinValueValidator

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class ContactMessage(models.Model):
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE, related_name='messages')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    property_type = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    budget = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField()
    newsletter = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.name} to {self.agent.name}"

class Agent(models.Model):
    SPECIALTY_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('luxury', 'Luxury Properties'),
        ('rental', 'Rental Properties'),
    ]
    
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    experience = models.PositiveIntegerField(help_text="Years of experience", validators=[MinValueValidator(1)])
    properties_sold = models.PositiveIntegerField(default=0)
    specialties = models.JSONField(default=list)
    linkedin_url = models.URLField(blank=True, null=True)
    whatsapp_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-experience', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.title}"
    
    @property
    def properties(self):
        return f"{self.properties_sold}+ Properties"