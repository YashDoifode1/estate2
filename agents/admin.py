from django.contrib import admin
from .models import Agent

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'experience', 'properties_sold', 'is_active']
    list_filter = ['specialties', 'is_active']
    search_fields = ['name', 'title', 'email']
    list_editable = ['is_active']