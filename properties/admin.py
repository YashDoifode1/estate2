from django.contrib import admin
from .models import SavedProperty
from django.utils.html import format_html
from .models import (
    Property,
    PropertyType,
    PropertyImage,
    Amenity,
    PropertyAmenity,
    NearbyPlace,
    PropertyView,
)

from django.contrib import admin
from .models import ScheduledVisit

@admin.register(ScheduledVisit)
class ScheduledVisitAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'email', 'phone', 'preferred_date', 'preferred_time', 'created_at')
    list_filter = ('preferred_date', 'created_at')
    search_fields = ('name', 'email', 'property__title')

from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)

# -----------------------------
# INLINE CLASSES
# -----------------------------
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ("image_preview", "image", "alt_text", "is_primary", "order")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="60" style="object-fit:cover;border-radius:4px;"/>',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity
    extra = 1
    autocomplete_fields = ["amenity"]


class NearbyPlaceInline(admin.TabularInline):
    model = NearbyPlace
    extra = 1


# -----------------------------
# MAIN PROPERTY ADMIN
# -----------------------------
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "property_id",
        "thumbnail",
        "title",
        "get_type_display_name",
        "status",
        "price",
        "city",
        "is_active",
        "featured",
        "created_at",
    )
    list_filter = ("status", "type", "custom_type", "featured", "is_active", "city", "created_at")
    search_fields = ("title", "property_id", "location", "description")
    list_editable = ("status", "is_active", "featured")
    readonly_fields = ("property_id", "created_at", "updated_at")
    inlines = [PropertyImageInline, PropertyAmenityInline, NearbyPlaceInline]
    ordering = ("-featured", "-created_at")
    list_per_page = 25

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "property_id", "title", "description", "status", 
                "type", "custom_type", "price", "price_per_sqft"
            )
        }),
        ("Location", {
            "fields": ("location", "city", "state", "pincode", "latitude", "longitude", "location_description")
        }),
        ("Property Details", {
            "fields": (
                "total_area", "built_up_area", "bedrooms", "bathrooms", 
                "balconies", "garage", "floors", "floor_number",
                "year_built", "furnishing"
            )
        }),
        ("Additional", {
            "fields": ("featured", "featured_until", "is_active", "agent")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def thumbnail(self, obj):
        """Show a small primary image beside each property in list view"""
        primary = obj.images.filter(is_primary=True).first()
        if primary and primary.image:
            return format_html(
                '<img src="{}" width="70" height="50" style="object-fit:cover;border-radius:4px;"/>',
                primary.image.url
            )
        return "—"
    thumbnail.short_description = "Image"

    def get_type_display_name(self, obj):
        """Display custom type if set, otherwise fallback to default choice"""
        return obj.custom_type.name if obj.custom_type else obj.get_type_display()
    get_type_display_name.short_description = "Type"


# -----------------------------
# PROPERTY TYPE ADMIN
# -----------------------------
@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20


# -----------------------------
# AMENITY ADMIN
# -----------------------------
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon_class", "category")
    list_filter = ("category",)
    search_fields = ("name", "category")


# -----------------------------
# PROPERTY VIEW ADMIN
# -----------------------------
@admin.register(PropertyView)
class PropertyViewAdmin(admin.ModelAdmin):
    list_display = ("property", "ip_address", "viewed_at")
    list_filter = ("viewed_at",)
    readonly_fields = ("property", "ip_address", "user_agent", "viewed_at")
    search_fields = ("property__title", "ip_address")
    ordering = ("-viewed_at",)


@admin.register(SavedProperty)
class SavedPropertyAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__email', 'property__title')