"""
DreamHomes Realty - Simplified Django Settings
(No .env and no extra security layers)
"""

import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# =============================================================================
# BASE SETTINGS
# =============================================================================
SECURE_SSL_REDIRECT = False

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_random_secret_key()
DEBUG = True
ALLOWED_HOSTS = ["*"]

# =============================================================================
# APPLICATIONS
# =============================================================================

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',

    # Local apps
    'accounts',
    'properties',
    'agents',
    'blog',
]

# =============================================================================
# MIDDLEWARE
# =============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dreamhomes.urls'
WSGI_APPLICATION = 'dreamhomes.wsgi.application'

# =============================================================================
# TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dreamhomes.context_processors.current_year',
                'dreamhomes.context_processors.company_info',
            ],
        },
    },
]

# =============================================================================
# DATABASE
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# =============================================================================
# AUTHENTICATION
# =============================================================================

AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC & MEDIA
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# EMAIL (Console for testing)
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@dreamhomesrealty.com'

# =============================================================================
# COMPANY INFO (Hardcoded for simplicity)
# =============================================================================

COMPANY_INFO = {
    "NAME": "DreamHomes Realty",
    "TAGLINE": "Your trusted partner in real estate.",
    "ADDRESS": "123 Civil Lines, Nagpur, Maharashtra 440001",
    "PHONE": "+91 98765 43210",
    "EMAIL": "info@dreamhomesrealty.com",
    "HOURS": "Mon - Sat: 9:00 AM - 7:00 PM",
    "FACEBOOK": "https://facebook.com/dreamhomes",
    "TWITTER": "https://twitter.com/dreamhomes",
    "INSTAGRAM": "https://instagram.com/dreamhomes",
    "LINKEDIN": "https://linkedin.com/company/dreamhomes",
}

# =============================================================================
# JAZZMIN ADMIN SETTINGS
# =============================================================================

JAZZMIN_SETTINGS = {
    "site_title": "DreamHomes Admin",
    "site_header": "DreamHomes Realty",
    "site_brand": "DreamHomes",
    "site_icon": "images/favicon.ico",
    "welcome_sign": "Welcome to DreamHomes Admin Dashboard",
    "copyright": "DreamHomes Realty",
    "search_model": "properties.Property",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar": "navbar-dark bg-primary",
    "sidebar_fixed": True,
}

# =============================================================================
# COMPANY INFO (Hardcoded for simplicity)
# =============================================================================

# =============================================================================
# COMPANY INFO (Extended)
# =============================================================================

COMPANY_INFO = {
    "NAME": "DreamHomes Realty",
    "TAGLINE": "Your trusted partner in real estate.",
    "ADDRESS": "123 Real Estate Avenue, Civil Lines, Nagpur, Maharashtra 440001",
    "PHONES": ["+91 98765 43210", "+91 71234 56789"],
    "EMAILS": ["info@dreamhomesrealty.com", "sales@dreamhomesrealty.com"],
    "HOURS": {
        "WEEKDAYS": "Monday - Friday: 9:00 AM - 6:00 PM",
        "SATURDAY": "Saturday: 10:00 AM - 4:00 PM",
        "SUNDAY": "Sunday: Closed",
    },
    "EMERGENCY_PHONE": "+91 98765 43210",
    "OFFICE_LOCATION": {
        "lat": 21.1458,
        "lng": 79.0882,
        "heading": 210,
        "pitch": 5,
        "fov": 80,
    },
    "TEAM_MEMBERS": [
        {
            "name": "Rahul Sharma",
            "position": "Founder & CEO",
            "description": "Leading DreamHomes Realty with over 15 years of experience in the Nagpur real estate market.",
            "image_url": "https://randomuser.me/api/portraits/men/45.jpg",
            "email": "rahul@dreamhomesrealty.com",
            "linkedin_url": "https://linkedin.com/in/rahulsharma",
            "twitter_url": "https://twitter.com/rahulsharma",
        },
        {
            "name": "Priya Deshmukh",
            "position": "Sales Director",
            "description": "Expert in residential and luxury property sales with a client-first approach.",
            "image_url": "https://randomuser.me/api/portraits/women/65.jpg",
            "email": "priya@dreamhomesrealty.com",
            "linkedin_url": "https://linkedin.com/in/priyadeshmukh",
            "twitter_url": "https://twitter.com/priyadeshmukh",
        },
        {
            "name": "Arjun Mehta",
            "position": "Marketing Manager",
            "description": "Drives creative campaigns that help clients connect with their dream homes.",
            "image_url": "https://randomuser.me/api/portraits/men/33.jpg",
            "email": "arjun@dreamhomesrealty.com",
            "linkedin_url": "https://linkedin.com/in/arjunmehta",
            "twitter_url": "https://twitter.com/arjunmehta",
        },
        {
            "name": "Neha Patil",
            "position": "Customer Relations Head",
            "description": "Ensures every client receives outstanding support throughout their real estate journey.",
            "image_url": "https://randomuser.me/api/portraits/women/52.jpg",
            "email": "neha@dreamhomesrealty.com",
            "linkedin_url": "https://linkedin.com/in/nehapatil",
            "twitter_url": "https://twitter.com/nehapatil",
        },
    ],
}



# =============================================================================
# OTHER SETTINGS
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Optional check in console
print("✅ Django loaded successfully (DEBUG mode ON)")
print(f"Company: {COMPANY_INFO['NAME']}")
