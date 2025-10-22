from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('api/', views.get_properties_api, name='get_properties'),
    path('<int:pk>/<slug:slug>/', views.property_detail, name='property_detail'),
    path('<int:property_id>/schedule-visit/', views.schedule_visit, name='schedule_visit'),
    path('<int:property_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_properties, name='favorite_properties'),
    path('contact/', views.contact, name='contact'),  # Add contact here
]