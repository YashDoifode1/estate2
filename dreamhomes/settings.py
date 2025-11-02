"""
DreamHomes Realty - Django Settings
Windows-compatible development version
"""

import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# CORE SECURITY SETTINGS
# =============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'false'

# Hosts/domain names that this Django site can serve
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

INSTALLED_APPS = [
    'jazzmin',  # Admin interface
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',  # SEO: Sitemap support
    'django.contrib.humanize',  # Better template formatting
    
    # Local apps
    'accounts',
    'properties',
    'agents',
    'blog',
]

# =============================================================================
# MIDDLEWARE CONFIGURATION
# =============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============================================================================
# URL & WSGI CONFIGURATION
# =============================================================================

ROOT_URLCONF = 'dreamhomes.urls'
WSGI_APPLICATION = 'dreamhomes.wsgi.application'

# =============================================================================
# TEMPLATE CONFIGURATION
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
# DATABASE CONFIGURATION (SQLite for Windows development)
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# CUSTOM USER MODEL
# =============================================================================

AUTH_USER_MODEL = 'accounts.CustomUser'

# =============================================================================
# AUTHENTICATION & SESSION SETTINGS
# =============================================================================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Security settings for production (disabled in development)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# =============================================================================
# EMAIL CONFIGURATION (Development - Console backend)
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@dreamhomesrealty.com'

# =============================================================================
# JAZZMIN ADMIN CONFIGURATION
# =============================================================================

JAZZMIN_SETTINGS = {
    "site_title": "DreamHomes Admin",
    "site_header": "DreamHomes Realty",
    "site_brand": "DreamHomes",
    # "site_logo": "images/favicon.jpeg",
    "site_icon": "images/favicon.ico",
    "welcome_sign": "Welcome to DreamHomes Admin Dashboard",
    "copyright": "DreamHomes Realty",
    "search_model": "properties.Property",
    "user_avatar": None,

    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "properties"},
        {"app": "agents"},
        {"app": "blog"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["properties", "agents", "blog", "auth"],

    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users-cog",
        "blog.BlogPost": "fas fa-newspaper",
        "properties.Property": "fas fa-home",
        "properties.PropertyType": "fas fa-building",
        "properties.PropertyImage": "fas fa-image",
        "properties.Amenity": "fas fa-list",
        "agents.Agent": "fas fa-user-tie",
    },

    "related_modal_active": True,
    "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar": "navbar-dark bg-primary",
    "sidebar_fixed": True,
}

# =============================================================================
# CACHE CONFIGURATION (Simple memory cache for development)
# =============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# =============================================================================
# SEO & SITE SETTINGS
# =============================================================================

SITE_NAME = "DreamHomes Realty"
SITE_DESCRIPTION = "Find your dream home with DreamHomes Realty"
SITE_KEYWORDS = "real estate, properties, homes for sale, apartment rental"

# =============================================================================
# DEFAULT AUTO FIELD
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# FOOTER COMPANY INFO (Loaded from environment variables)
# =============================================================================

COMPANY_INFO = {
    "NAME": os.getenv("COMPANY_NAME", "DreamHomes Realty"),
    "TAGLINE": os.getenv("COMPANY_TAGLINE", "Your trusted partner in real estate."),
    "ADDRESS": os.getenv("COMPANY_ADDRESS", "Nagpur, India"),
    "PHONE": os.getenv("COMPANY_PHONE", "+91 98765 43210"),
    "EMAIL": os.getenv("COMPANY_EMAIL", "info@dreamhomesrealty.com"),
    "HOURS": os.getenv("COMPANY_HOURS", "Mon - Sat: 9:00 AM - 7:00 PM"),
    "FACEBOOK": os.getenv("FACEBOOK_URL", "#"),
    "TWITTER": os.getenv("TWITTER_URL", "#"),
    "INSTAGRAM": os.getenv("INSTAGRAM_URL", "#"),
    "LINKEDIN": os.getenv("LINKEDIN_URL", "#"),
}
