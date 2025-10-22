from django.contrib import admin
from .models import Property, PropertyType, Amenity, PropertyImage, NearbyPlace, PropertyView, FavoriteProperty

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class NearbyPlaceInline(admin.TabularInline):
    model = NearbyPlace
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_id', 'property_type', 'status', 'price', 'location', 'featured', 'is_active']
    list_filter = ['status', 'property_type', 'featured', 'is_active', 'created_at']
    search_fields = ['title', 'property_id', 'location', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyImageInline, NearbyPlaceInline]
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_class']
    search_fields = ['name']

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_class']
    search_fields = ['name']

@admin.register(PropertyView)
class PropertyViewAdmin(admin.ModelAdmin):
    list_display = ['property', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    readonly_fields = ['viewed_at']

@admin.register(FavoriteProperty)
class FavoritePropertyAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'added_at']
    list_filter = ['added_at']
    readonly_fields = ['added_at']