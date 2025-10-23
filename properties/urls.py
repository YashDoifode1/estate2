from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('get-properties/', views.get_properties, name='get_properties'),  # This line was missing
    path('<int:property_id>/', views.property_detail, name='property_detail'),
    path('<int:property_id>/schedule-visit/', views.schedule_visit, name='schedule_visit'),
    path('contact/', views.contact_view, name='contact'),
]