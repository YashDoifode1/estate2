from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from properties.views import contact  # Update this import
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from .sitemap import StaticViewSitemap, PropertySitemap, BlogSitemap
import os
from django.conf import settings

# Sitemaps configuration
sitemaps = {
    'static': StaticViewSitemap,
    'properties': PropertySitemap,
    'blog': BlogSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('agents/', include('agents.urls', namespace='agents')),
    path('properties/', include('properties.urls', namespace='properties')),  # Add this line
    
    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    
    # Legal pages
    path('terms/', account_views.terms, name='terms'),
    path('privacy/', account_views.privacy, name='privacy'),
    
    # Contact page - now handled by properties app
    path('contact/', contact, name='contact'),
    
    # Keep only accounts-related pages
    path('', account_views.home, name='home'),
    path('about/', account_views.about, name='about'),
    
    path('settings/', account_views.settings, name='settings'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += [
        path('robots.txt', serve, {
            'path': 'robots.txt',
            'document_root': settings.BASE_DIR,
            'content_type': 'text/plain'
        }),
    ]