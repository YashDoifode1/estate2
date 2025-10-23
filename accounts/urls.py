# accounts/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    
    # Profile Actions
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    
    # Settings Actions
    path('settings/update-profile/', views.update_profile, name='update_profile'),
    path('settings/update-password/', views.update_password, name='update_password'),
    path('settings/update-preferences/', views.update_preferences, name='update_preferences'),
    path('settings/update-notifications/', views.update_notifications, name='update_notifications'),
    path('settings/update-privacy/', views.update_privacy, name='update_privacy'),
    path('settings/toggle-2fa/', views.toggle_2fa, name='toggle_2fa'),
    path('settings/download-data/', views.download_data, name='download_data'),
    path('settings/clear-history/', views.clear_history, name='clear_history'),
    path('settings/deactivate-account/', views.deactivate_account, name='deactivate_account'),
    path('settings/delete-account/', views.delete_account, name='delete_account'),
    
    # Property Actions
    path('toggle-save-property/', views.toggle_save_property, name='toggle_save_property'),
    path('remove-saved-property/', views.remove_saved_property, name='remove_saved_property'),
    
    # Notification Actions
    path('dismiss-notification/', views.dismiss_notification, name='dismiss_notification'),
    
    # Consultation Actions
    path('cancel-consultation/', views.cancel_consultation, name='cancel_consultation'),
    path('terminate-session/', views.terminate_session, name='terminate_session'),
path('terminate-all-sessions/', views.terminate_all_sessions, name='terminate_all_sessions'),
    # Password Reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]