from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Property, PropertyImage, Amenity, PropertyAmenity, NearbyPlace, PropertyView

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity
    extra = 1

class NearbyPlaceInline(admin.TabularInline):
    model = NearbyPlace
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['property_id', 'title', 'type', 'status', 'price', 'location', 'is_active', 'featured']
    list_filter = ['status', 'type', 'featured', 'is_active', 'city', 'created_at']
    search_fields = ['title', 'property_id', 'location', 'description']
    list_editable = ['status', 'is_active', 'featured']
    inlines = [PropertyImageInline, PropertyAmenityInline, NearbyPlaceInline]
    readonly_fields = ['property_id', 'created_at', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ['property_id', 'title', 'description', 'status', 'type', 'price', 'price_per_sqft']
        }),
        ('Location', {
            'fields': ['location', 'city', 'state', 'pincode', 'latitude', 'longitude', 'location_description']
        }),
        ('Property Details', {
            'fields': [
                'total_area', 'built_up_area', 'bedrooms', 'bathrooms', 
                'balconies', 'garage', 'floors', 'floor_number', 
                'year_built', 'furnishing'
            ]
        }),
        ('Additional', {
            'fields': ['featured', 'featured_until', 'is_active', 'agent']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_class', 'category']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(PropertyView)
class PropertyViewAdmin(admin.ModelAdmin):
    list_display = ['property', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    readonly_fields = ['property', 'ip_address', 'user_agent', 'viewed_at']