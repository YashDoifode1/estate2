from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import csv
from .models import CustomUser, UserProfile, UserPreferences, NotificationSettings, PrivacySettings, LoginSession, SavedProperty, Consultation, Notification
from .forms import CustomAuthenticationForm, CustomUserCreationForm, ProfilePictureForm, UserProfileForm, PasswordChangeForm, PreferencesForm, NotificationSettingsForm, PrivacySettingsForm, DeleteAccountForm, NewsletterForm, ProfileForm
from django.shortcuts import render
from properties.models import Property
from blog.models import BlogPost  # Correct import


from django.contrib.sessions.models import Session
from django.utils import timezone

@login_required
@require_POST
def terminate_session(request):
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        session = get_object_or_404(LoginSession, id=session_id, user=request.user)
        # Find and delete the corresponding Django session
        django_session = Session.objects.filter(session_key=session.session_key).first()
        if django_session:
            django_session.delete()
        session.delete()
        session_count = LoginSession.objects.filter(user=request.user).count()
        return JsonResponse({
            'success': True,
            'session_count': session_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_POST
def terminate_all_sessions(request):
    try:
        # Keep the current session active
        current_session_key = request.session.session_key
        sessions = LoginSession.objects.filter(user=request.user).exclude(session_key=current_session_key)
        for session in sessions:
            django_session = Session.objects.filter(session_key=session.session_key).first()
            if django_session:
                django_session.delete()
            session.delete()
        session_count = LoginSession.objects.filter(user=request.user).count()
        return JsonResponse({
            'success': True,
            'session_count': session_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def home(request):
    # Featured properties
    featured_properties = Property.objects.filter(featured=True).order_by('-created_at')[:6]
    # Latest blog posts (published only)
    latest_posts = BlogPost.objects.filter(status='published').order_by('-published_date')[:3]
    # Locations for the search form
    locations = Property.objects.filter(is_active=True).values_list('location', flat=True).distinct()

    context = {
        'featured_properties': featured_properties,
        'latest_posts': latest_posts,
        'locations': sorted([loc for loc in locations if loc]),
    }
    return render(request, 'accounts/home.html', context)

@login_required
def settings_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    preferences, created = UserPreferences.objects.get_or_create(user=request.user)
    notification_settings, created = NotificationSettings.objects.get_or_create(user=request.user)
    privacy_settings, created = PrivacySettings.objects.get_or_create(user=request.user)
    
    # Get active sessions
    sessions = LoginSession.objects.filter(user=request.user).order_by('-last_active')
    
    context = {
        'profile_form': UserProfileForm(instance=profile),
        'preferences_form': PreferencesForm(instance=preferences),
        'notifications_form': NotificationSettingsForm(instance=notification_settings),
        'privacy_form': PrivacySettingsForm(instance=privacy_settings),
        'password_form': PasswordChangeForm(request.user),
        'delete_form': DeleteAccountForm(request.user),
        'newsletter_form': NewsletterForm(),
        'sessions': sessions,
    }
    return render(request, 'accounts/settings.html', context)

from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm, ProfileForm

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            # Ensure username is never empty
            if not user.username:
                user.username = user.email
            user.save()
            profile_form.save()
            messages.success(request, "✅ Profile updated successfully.")
        else:
            print(user_form.errors, profile_form.errors)
            messages.error(request, "⚠️ Please fix the errors below.")

    return redirect('settings')


@login_required
@require_POST
def update_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    
    if form.is_valid():
        request.user.set_password(form.cleaned_data['new_password1'])
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Password updated successfully!')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('settings')

@login_required
@require_POST
def update_preferences(request):
    preferences, created = UserPreferences.objects.get_or_create(user=request.user)
    form = PreferencesForm(request.POST, instance=preferences)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Preferences updated successfully!')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('settings')

@login_required
@require_POST
def update_notifications(request):
    notification_settings, created = NotificationSettings.objects.get_or_create(user=request.user)
    form = NotificationSettingsForm(request.POST, instance=notification_settings)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Notification settings updated successfully!')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('settings')

@login_required
@require_POST
def update_privacy(request):
    privacy_settings, created = PrivacySettings.objects.get_or_create(user=request.user)
    form = PrivacySettingsForm(request.POST, instance=privacy_settings)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Privacy settings updated successfully!')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('settings')

@login_required
@require_POST
def toggle_2fa(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.two_factor_enabled = not profile.two_factor_enabled
    profile.save()
    
    action = "enabled" if profile.two_factor_enabled else "disabled"
    messages.success(request, f'Two-factor authentication {action}!')
    return redirect('settings')

@login_required
@require_POST
def download_data(request):
    # Create CSV response with user data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{request.user.email}_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Data Type', 'Details'])
    writer.writerow(['Email', request.user.email])
    writer.writerow(['First Name', request.user.first_name])
    writer.writerow(['Last Name', request.user.last_name])
    writer.writerow(['Phone', request.user.phone])
    writer.writerow(['Join Date', request.user.date_joined])
    
    # Add profile data
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    writer.writerow(['Location', profile.location])
    writer.writerow(['Bio', profile.bio])
    
    # Add saved properties count
    saved_count = SavedProperty.objects.filter(user=request.user).count()
    writer.writerow(['Saved Properties', saved_count])
    
    # Add consultations count
    consultations_count = Consultation.objects.filter(user=request.user).count()
    writer.writerow(['Consultations', consultations_count])
    
    messages.success(request, 'Your data has been prepared for download.')
    return response

@login_required
@require_POST
def clear_history(request):
    # Clear search history (you'll need to implement this based on your search model)
    # For now, this is a placeholder
    messages.success(request, 'Search history cleared successfully!')
    return redirect('settings')

@login_required
@require_POST
def deactivate_account(request):
    request.user.is_active = False
    request.user.save()
    messages.success(request, 'Your account has been deactivated.')
    return redirect('home')

@login_required
@require_POST
def delete_account(request):
    form = DeleteAccountForm(request.user, request.POST)
    
    if form.is_valid():
        # Delete user and all related data
        request.user.delete()
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('home')
    else:
        messages.error(request, 'Invalid password. Please try again.')
        return redirect('settings')

@login_required
@require_POST
def upload_profile_picture(request):
    form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def toggle_save_property(request):
    try:
        data = json.loads(request.body)
        property_id = data.get('property_id')
        
        # You'll need to implement this based on your Property model
        # For now, this is a placeholder
        saved_property, created = SavedProperty.objects.get_or_create(
            user=request.user,
            property_id=property_id
        )
        
        if not created:
            saved_property.delete()
            
        saved_count = request.user.saved_properties.count()
        return JsonResponse({
            'success': True,
            'saved_count': saved_count,
            'is_saved': created
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# ... include other views from previous implementation (login, register, profile, etc.)

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                remember_me = form.cleaned_data.get('remember_me')
                if not remember_me:
                    request.session.set_expiry(0)
                
                # Log login session
                LoginSession.objects.create(
                    user=user,
                    device=request.META.get('HTTP_USER_AGENT', 'Unknown'),
                    location=f"{request.META.get('REMOTE_ADDR', 'Unknown')}",
                    ip_address=request.META.get('REMOTE_ADDR', ''),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                return redirect('profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # include request.FILES
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    saved_properties = request.user.saved_properties.select_related('property').all()
    consultations = request.user.consultations.select_related('agent').all()
    notifications = request.user.notifications.filter(is_read=False)
    sessions = LoginSession.objects.filter(user=request.user).order_by('-last_active')
    
    context = {
        'company': Company.objects.first(),
        'saved_properties': saved_properties,
        'consultations': consultations,
        'notifications': notifications,
        'sessions': sessions,
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@require_POST
def toggle_save_property(request):
    try:
        data = json.loads(request.body)
        property_id = data.get('property_id')
        
        # You'll need to implement this based on your Property model
        # For now, this is a placeholder
        saved_property, created = SavedProperty.objects.get_or_create(
            user=request.user,
            property_id=property_id
        )
        
        if not created:
            saved_property.delete()
            
        saved_count = request.user.saved_properties.count()
        return JsonResponse({
            'success': True,
            'saved_count': saved_count,
            'is_saved': created
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_POST
def remove_saved_property(request):
    try:
        data = json.loads(request.body)
        property_id = data.get('property_id')
        
        SavedProperty.objects.filter(
            user=request.user,
            property_id=property_id
        ).delete()
        
        saved_count = request.user.saved_properties.count()
        return JsonResponse({
            'success': True,
            'saved_count': saved_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_POST
def dismiss_notification(request):
    try:
        data = json.loads(request.body)
        notification_id = data.get('notification_id')
        
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        
        notification_count = request.user.notifications.filter(is_read=False).count()
        return JsonResponse({
            'success': True,
            'notification_count': notification_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_POST
def cancel_consultation(request):
    try:
        data = json.loads(request.body)
        consultation_id = data.get('consultation_id')
        
        consultation = get_object_or_404(Consultation, id=consultation_id, user=request.user)
        consultation.status = 'cancelled'
        consultation.save()
        
        consultation_count = request.user.consultations.filter(status='scheduled').count()
        return JsonResponse({
            'success': True,
            'consultation_count': consultation_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def terms(request):
    return render(request, 'accounts/terms.html')

def privacy(request):
    return render(request, 'accounts/privacy.html')


from django.shortcuts import render
from properties.models import Property  # Your property model


from django.shortcuts import render
from datetime import datetime

def about(request):
    # Timeline milestones data (you can later move this to a model)
    milestones = [
        {
            "year": "2008",
            "title": "Founded DreamHomes Realty",
            "description": "Started as a small local agency with a vision to simplify real estate transactions in Nagpur."
        },
        {
            "year": "2012",
            "title": "Expanded to Commercial Real Estate",
            "description": "Entered the commercial sector, helping businesses find premium office spaces."
        },
        {
            "year": "2016",
            "title": "Reached 1000+ Clients",
            "description": "A proud moment as we crossed the milestone of serving over 1000 satisfied clients."
        },
        {
            "year": "2020",
            "title": "Digital Transformation",
            "description": "Launched our online property platform for a seamless search and inquiry experience."
        },
        {
            "year": "2024",
            "title": "Awarded Best Realty Agency in Nagpur",
            "description": "Recognized for excellence, transparency, and customer satisfaction."
        },
    ]

    # Team members data (can later come from a database model like TeamMember)
    team_members = [
        {
            "name": "Rohan Sharma",
            "position": "Founder & CEO",
            "description": "With over 15 years of real estate experience, Rohan leads DreamHomes with a focus on trust and innovation.",
            "image_url": "https://randomuser.me/api/portraits/men/32.jpg",
            "linkedin_url": "https://linkedin.com/in/rohan-sharma",
            "twitter_url": "https://twitter.com/rohan_sharma",
            "email": "rohan@dreamhomesrealty.com"
        },
        {
            "name": "Neha Verma",
            "position": "Head of Sales",
            "description": "Neha specializes in residential properties and customer success management.",
            "image_url": "https://randomuser.me/api/portraits/women/44.jpg",
            "linkedin_url": "https://linkedin.com/in/neha-verma",
            "twitter_url": "https://twitter.com/neha_verma",
            "email": "neha@dreamhomesrealty.com"
        },
        {
            "name": "Amit Patel",
            "position": "Marketing Director",
            "description": "Amit drives our marketing and brand strategy, ensuring DreamHomes stays top-of-mind in Nagpur.",
            "image_url": "https://randomuser.me/api/portraits/men/47.jpg",
            "linkedin_url": "https://linkedin.com/in/amit-patel",
            "twitter_url": "https://twitter.com/amit_patel",
            "email": "amit@dreamhomesrealty.com"
        },
        {
            "name": "Sneha Kulkarni",
            "position": "Client Relations Manager",
            "description": "Sneha ensures every client receives personalized attention and support throughout their property journey.",
            "image_url": "https://randomuser.me/api/portraits/women/65.jpg",
            "linkedin_url": "https://linkedin.com/in/sneha-kulkarni",
            "twitter_url": "https://twitter.com/sneha_kulkarni",
            "email": "sneha@dreamhomesrealty.com"
        },
    ]

    context = {
        "milestones": milestones,
        "team_members": team_members,
        "now": datetime.now(),  # used in footer © year
    }

    return render(request, 'accounts/about.html', context)




def blog_list(request):
    return render(request, 'accounts/blog_list.html')

def settings(request):
    return render(request, 'accounts/settings.html')



# ____________________________________________________


# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import csv

# Import your models and forms
from .models import CustomUser, UserProfile, UserPreferences, NotificationSettings, PrivacySettings, LoginSession, SavedProperty, Consultation, Notification
from .forms import CustomAuthenticationForm, CustomUserCreationForm, ProfilePictureForm, UserProfileForm, PasswordChangeForm, PreferencesForm, NotificationSettingsForm, PrivacySettingsForm, DeleteAccountForm, NewsletterForm, ProfileForm

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                remember_me = form.cleaned_data.get('remember_me')
                if not remember_me:
                    request.session.set_expiry(0)
                
                # Log login session
                LoginSession.objects.create(
                    user=user,
                    device=request.META.get('HTTP_USER_AGENT', 'Unknown'),
                    location=f"{request.META.get('REMOTE_ADDR', 'Unknown')}",
                    ip_address=request.META.get('REMOTE_ADDR', ''),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    session_key=request.session.session_key
                )
                
                return redirect('profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# Profile Views
@login_required
def profile_view(request):
    try:
        saved_properties = request.user.saved_properties.select_related('property').all()
    except:
        saved_properties = []
    
    try:
        consultations = request.user.consultations.select_related('agent').all()
    except:
        consultations = []
    
    try:
        notifications = request.user.notifications.filter(is_read=False)
    except:
        notifications = []
    
    context = {
        'saved_properties': saved_properties,
        'consultations': consultations,
        'notifications': notifications,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def settings_view(request):
    # Get or create user profiles with error handling
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except Exception as e:
        profile = UserProfile(user=request.user)
        profile.save()
    
    try:
        preferences, created = UserPreferences.objects.get_or_create(user=request.user)
    except Exception as e:
        preferences = UserPreferences(user=request.user)
        preferences.save()
    
    try:
        notification_settings, created = NotificationSettings.objects.get_or_create(user=request.user)
    except Exception as e:
        notification_settings = NotificationSettings(user=request.user)
        notification_settings.save()
    
    try:
        privacy_settings, created = PrivacySettings.objects.get_or_create(user=request.user)
    except Exception as e:
        privacy_settings = PrivacySettings(user=request.user)
        privacy_settings.save()
    
    # Get active sessions
    try:
        sessions = LoginSession.objects.filter(user=request.user).order_by('-last_active')
    except:
        sessions = []
    
    context = {
        'profile_form': UserProfileForm(instance=profile),
        'preferences_form': PreferencesForm(instance=preferences),
        'notifications_form': NotificationSettingsForm(instance=notification_settings),
        'privacy_form': PrivacySettingsForm(instance=privacy_settings),
        'password_form': PasswordChangeForm(request.user),
        'delete_form': DeleteAccountForm(request.user),
        'newsletter_form': NewsletterForm(),
        'sessions': sessions,
    }
    return render(request, 'accounts/settings.html', context)

# Settings Action Views
@login_required
@require_POST
def update_profile(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, instance=profile)
    except Exception as e:
        form = UserProfileForm(request.POST)
    
    if form.is_valid():
        try:
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, 'Error saving profile. Please try again.')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('settings')

@login_required
@require_POST
def update_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    
    if form.is_valid():
        request.user.set_password(form.cleaned_data['new_password1'])
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Password updated successfully!')
    else:
        for error in form.errors.values():
            messages.error(request, error)
    
    return redirect('settings')

@login_required
@require_POST
def update_preferences(request):
    try:
        preferences, created = UserPreferences.objects.get_or_create(user=request.user)
        form = PreferencesForm(request.POST, instance=preferences)
    except Exception as e:
        form = PreferencesForm(request.POST)
    
    if form.is_valid():
        try:
            preferences = form.save(commit=False)
            preferences.user = request.user
            preferences.save()
            messages.success(request, 'Preferences updated successfully!')
        except Exception as e:
            messages.error(request, 'Error saving preferences. Please try again.')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('settings')

@login_required
@require_POST
def update_notifications(request):
    try:
        notification_settings, created = NotificationSettings.objects.get_or_create(user=request.user)
        form = NotificationSettingsForm(request.POST, instance=notification_settings)
    except Exception as e:
        form = NotificationSettingsForm(request.POST)
    
    if form.is_valid():
        try:
            notification_settings = form.save(commit=False)
            notification_settings.user = request.user
            notification_settings.save()
            messages.success(request, 'Notification settings updated successfully!')
        except Exception as e:
            messages.error(request, 'Error saving notification settings. Please try again.')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('settings')

@login_required
@require_POST
def update_privacy(request):
    try:
        privacy_settings, created = PrivacySettings.objects.get_or_create(user=request.user)
        form = PrivacySettingsForm(request.POST, instance=privacy_settings)
    except Exception as e:
        form = PrivacySettingsForm(request.POST)
    
    if form.is_valid():
        try:
            privacy_settings = form.save(commit=False)
            privacy_settings.user = request.user
            privacy_settings.save()
            messages.success(request, 'Privacy settings updated successfully!')
        except Exception as e:
            messages.error(request, 'Error saving privacy settings. Please try again.')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('settings')

@login_required
@require_POST
def toggle_2fa(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.two_factor_enabled = not profile.two_factor_enabled
        profile.save()
        
        action = "enabled" if profile.two_factor_enabled else "disabled"
        messages.success(request, f'Two-factor authentication {action}!')
    except Exception as e:
        messages.error(request, 'Error updating two-factor authentication settings.')
    
    return redirect('settings')

@login_required
@require_POST
def download_data(request):
    # Create CSV response with user data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{request.user.email}_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Data Type', 'Details'])
    writer.writerow(['Email', request.user.email])
    writer.writerow(['First Name', request.user.first_name])
    writer.writerow(['Last Name', request.user.last_name])
    writer.writerow(['Phone', request.user.phone])
    writer.writerow(['Join Date', request.user.date_joined])
    
    # Add profile data if available
    try:
        profile = UserProfile.objects.get(user=request.user)
        writer.writerow(['Location', profile.location])
        writer.writerow(['Bio', profile.bio])
    except:
        pass
    
    messages.success(request, 'Your data has been prepared for download.')
    return response

@login_required
@require_POST
def clear_history(request):
    # This is a placeholder - implement based on your search history model
    messages.success(request, 'Search history cleared successfully!')
    return redirect('settings')

@login_required
@require_POST
def deactivate_account(request):
    request.user.is_active = False
    request.user.save()
    messages.success(request, 'Your account has been deactivated.')
    return redirect('home')

@login_required
@require_POST
def delete_account(request):
    form = DeleteAccountForm(request.user, request.POST)
    
    if form.is_valid():
        # Delete user and all related data
        request.user.delete()
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('home')
    else:
        messages.error(request, 'Invalid password. Please try again.')
        return redirect('settings')

# AJAX Action Views
@login_required
@require_POST
def upload_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()  # updates profile_picture and updated_at
    return redirect('profile')

@login_required
@require_POST
def toggle_save_property(request):
    try:
        data = json.loads(request.body)
        property_id = data.get('property_id')
        
        # This is a placeholder - implement based on your Property model
        saved_property, created = SavedProperty.objects.get_or_create(
            user=request.user,
            property_id=property_id
        )
        
        if not created:
            saved_property.delete()
            
        saved_count = SavedProperty.objects.filter(user=request.user).count()
        return JsonResponse({
            'success': True,
            'saved_count': saved_count,
            'is_saved': created
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_POST
def remove_saved_property(request):
    try:
        data = json.loads(request.body)
        property_id = data.get('property_id')
        
        SavedProperty.objects.filter(
            user=request.user,
            property_id=property_id
        ).delete()
        
        saved_count = SavedProperty.objects.filter(user=request.user).count()
        return JsonResponse({
            'success': True,
            'saved_count': saved_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_POST
def dismiss_notification(request):
    try:
        data = json.loads(request.body)
        notification_id = data.get('notification_id')
        
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        
        notification_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({
            'success': True,
            'notification_count': notification_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_POST
def cancel_consultation(request):
    try:
        data = json.loads(request.body)
        consultation_id = data.get('consultation_id')
        
        consultation = get_object_or_404(Consultation, id=consultation_id, user=request.user)
        consultation.status = 'cancelled'
        consultation.save()
        
        consultation_count = Consultation.objects.filter(user=request.user, status='scheduled').count()
        return JsonResponse({
            'success': True,
            'consultation_count': consultation_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})