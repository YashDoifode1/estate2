"""
DreamHomes Realty - Django Settings
Production-ready configuration with security, performance, and SEO optimizations
"""

import os
import environ
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read environment file
environ.Env.read_env(BASE_DIR / '.env')

# =============================================================================
# CORE SECURITY SETTINGS
# =============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)

# Hosts/domain names that this Django site can serve
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# CSRF trusted origins for production
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',  # SEO: Sitemap support
    'django.contrib.humanize',  # Better template formatting
]

THIRD_PARTY_APPS = [
    'jazzmin',           # Admin interface
    'compressor',        # CSS/JS compression
    'django_cleanup',    # Auto-delete old files
    'corsheaders',       # CORS headers for APIs
]

LOCAL_APPS = [
    'accounts',
    'properties',
    'agents',
    'blog',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# =============================================================================
# MIDDLEWARE CONFIGURATION
# =============================================================================

MIDDLEWARE = [
    # Security middleware - should be first
    'django.middleware.security.SecurityMiddleware',
    
    # Performance: WhiteNoise for static files (after SecurityMiddleware)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    # CORS middleware (before CommonMiddleware)
    'corsheaders.middleware.CorsMiddleware',
    
    # Django core middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Security: Clickjacking protection
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Security: Content sniffing protection
    'django.middleware.security.SecurityMiddleware',
    
    # Custom middleware (if any)
    # 'dreamhomes.middleware.SEOMiddleware',
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
                
                # Custom context processors
                'dreamhomes.context_processors.current_year',
                'dreamhomes.context_processors.site_info',  # For SEO meta tags
                'dreamhomes.context_processors.google_analytics',  # Analytics
            ],
            'builtins': [
                'dreamhomes.templatetags.seo_tags',  # Custom SEO template tags
            ],
        },
    },
]

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# Default SQLite configuration (development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,  # SQLite timeout
        }
    }
}

# PostgreSQL configuration for production (uncomment when deploying)
"""
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///dreamhomes'),
}
"""

# Database performance optimizations
DATABASES['default']['CONN_MAX_AGE'] = 60  # Persistent connections
DATABASES['default']['ATOMIC_REQUESTS'] = True  # Transaction per request

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'max_similarity': 0.7,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Password hashing (Argon2 is more secure than PBKDF2)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # Changed to IST for Indian audience
USE_I18N = True
USE_L10N = True
USE_TZ = True

# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',  # Django-compressor
]

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

# Session security
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Security settings for production
if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@dreamhomesrealty.com')
SERVER_EMAIL = env('SERVER_EMAIL', default='admin@dreamhomesrealty.com')

# =============================================================================
# CACHE CONFIGURATION
# =============================================================================

# Redis cache for production (uncomment when deploying)
"""
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
"""

# Local memory cache (development)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Cache timeout for various components
CACHE_MIDDLEWARE_SECONDS = 300  # 5 minutes

# =============================================================================
# JAZZMIN ADMIN CONFIGURATION
# =============================================================================

JAZZMIN_SETTINGS = {
    # Site configuration
    "site_title": "DreamHomes Admin",
    "site_header": "DreamHomes Realty",
    "site_brand": "DreamHomes",
    "site_logo": "images/favicon.jpeg",
    "site_icon": "images/favicon.ico",
    "welcome_sign": "Welcome to DreamHomes Admin Dashboard",
    "copyright": "DreamHomes Realty",
    "search_model": "properties.Property",
    "user_avatar": None,

    # Top navigation
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "properties"},
        {"app": "agents"},
        {"app": "blog"},
    ],

    # Sidebar customization
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["properties", "agents", "blog", "auth"],

    # Icons
    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users-cog",
        "blog.BlogPost": "fas fa-newspaper",
        "blog.BlogCategory": "fas fa-tags",
        "properties.Property": "fas fa-home",
        "properties.PropertyType": "fas fa-building",
        "properties.PropertyImage": "fas fa-image",
        "properties.Amenity": "fas fa-list",
        "agents.Agent": "fas fa-user-tie",
    },

    # UI features
    "related_modal_active": True,
    "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar_small_text": False,
    "footer_small_text": True,
    "accent": "blue",
    "navbar": "navbar-dark bg-primary",
    "sidebar_fixed": True,
    "theme_switcher": True,
}

# =============================================================================
# PERFORMANCE & OPTIMIZATION
# =============================================================================

# Django-compressor settings
COMPRESS_ENABLED = not DEBUG
COMPRESS_OFFLINE = not DEBUG
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# Database query logging (development only)
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console'],
            },
        },
    }

# =============================================================================
# SECURITY HEADERS
# =============================================================================

# Content Security Policy (CSP) - Basic setup
SECURE_CSP = {
    "default-src": ["'self'"],
    "style-src": ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"],
    "script-src": ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"],
    "img-src": ["'self'", "data:", "https:"],
}

# =============================================================================
# SEO & SITEMAP CONFIGURATION
# =============================================================================

# Site information for SEO
SITE_NAME = "DreamHomes Realty"
SITE_DESCRIPTION = "Find your dream home with DreamHomes Realty - Premium properties for sale and rent"
SITE_KEYWORDS = "real estate, properties, homes for sale, apartment rental, dream homes"
SITE_AUTHOR = "DreamHomes Realty"

# Sitemap configuration
SITEMAP_URL_SCHEME = 'https'

# Google Analytics (set in environment variables)
GOOGLE_ANALYTICS_ID = env('GOOGLE_ANALYTICS_ID', default='')

# =============================================================================
# CORS SETTINGS
# =============================================================================

CORS_ALLOWED_ORIGINS = [
    "https://dreamhomesrealty.com",
    "https://www.dreamhomesrealty.com",
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
]

# =============================================================================
# FILE UPLOAD SETTINGS
# =============================================================================

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000   # Maximum number of fields

# =============================================================================
# DEFAULT AUTO FIELD
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CUSTOM SETTINGS
# =============================================================================

# Property-related settings
PROPERTIES_PER_PAGE = 12
FEATURED_PROPERTIES_LIMIT = 6
SIMILAR_PROPERTIES_LIMIT = 4

# Agent settings
AGENTS_PER_PAGE = 9

# Blog settings
BLOG_POSTS_PER_PAGE = 6
RECENT_POSTS_LIMIT = 3