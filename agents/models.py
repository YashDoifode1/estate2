from django.db import models
from django.core.validators import MinValueValidator

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