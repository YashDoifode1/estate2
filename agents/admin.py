from django.contrib import admin
from .models import Agent
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'agent', 'created_at']
    list_filter = ['agent', 'created_at']
    search_fields = ['name', 'email', 'message']

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'experience', 'properties_sold', 'is_active']
    list_filter = ['specialties', 'is_active']
    search_fields = ['name', 'title', 'email']
    list_editable = ['is_active']