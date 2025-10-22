from django.urls import path
from . import views

app_name = 'agents'  # This creates the namespace

urlpatterns = [
    path('', views.agents_list, name='agents_list'),
    path('contact/<int:agent_id>/', views.contact_agent, name='contact_agent'),
]