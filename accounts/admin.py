from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, SavedProperty, Consultation, Notification

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'newsletter_subscription')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Preferences', {'fields': ('newsletter_subscription', 'terms_accepted')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'newsletter_subscription', 'terms_accepted'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'location')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'location')

@admin.register(SavedProperty)
class SavedPropertyAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__email', 'property__title')

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('user', 'agent', 'title', 'date', 'time', 'status')
    list_filter = ('status', 'mode', 'date')
    search_fields = ('user__email', 'agent__email', 'title')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('user__email', 'title')