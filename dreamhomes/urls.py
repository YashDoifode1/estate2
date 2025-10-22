from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from properties.views import contact  # Import the specific view directly
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('properties/', include('properties.urls')),
    
    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    
    # Legal pages
    path('terms/', account_views.terms, name='terms'),
    path('privacy/', account_views.privacy, name='privacy'),
    
    # Contact page
    path('contact/', contact, name='contact'),  # Use the directly imported view
    
    # Temporary placeholder views for navigation
    path('', account_views.home, name='home'),
    path('about/', account_views.about, name='about'),
    path('agents/', account_views.agents_list, name='agents_list'),
    path('blog/', account_views.blog_list, name='blog_list'),
    path('settings/', account_views.settings, name='settings'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)