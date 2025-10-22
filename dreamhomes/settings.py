import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "jazzmin",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'properties',
    'agents',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dreamhomes.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'dreamhomes.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Login/Logout URLs
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply@dreamhomesrealty.com'

# Remove CONTACT_EMAIL if it's causing issues, or make sure it's defined
# CONTACT_EMAIL = 'contact@dreamhomesrealty.com'

# For production, use:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.your-email-provider.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@example.com'
# EMAIL_HOST_PASSWORD = 'your-email-password'
# DEFAULT_FROM_EMAIL = 'your-email@example.com'

# settings.py
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS

# Production settings (to be implemented)
# 

# Jazzmin configuration
JAZZMIN_SETTINGS = {
    "site_title": "DreamHomes Admin",
    "site_header": "DreamHomes Realty",
    "site_brand": "DreamHomes",
    "site_logo": "images/favicon.ico",  # Add your admin logo in static/images/
    "login_logo": "images/favicon.ico",
    "login_logo_dark": None,
    "site_icon": "images/favicon.ico",
    "welcome_sign": "Welcome to DreamHomes Admin",
    "copyright": "DreamHomes Realty © 2025",
    "search_model": "blog.BlogPost",
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "blog.BlogPost"},
        {"app": "properties"},
        {"app": "agents"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["properties", "agents", "blog", "contact"],
    "custom_links": {},
    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users-cog",
        "blog.BlogPost": "fas fa-newspaper",
        "blog.BlogCategory": "fas fa-tags",
        "blog.BlogTag": "fas fa-tag",
        "blog.BlogComment": "fas fa-comments",
        "properties.Property": "fas fa-home",
        "properties.Amenities": "fas fa-list",
        "agents.Agent": "fas fa-user-tie",
        "contact.Contact": "fas fa-envelope",
    },
    "related_modal_active": True,
    "show_ui_builder": True,
}

# Optional: custom colors for theme
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",  # other options: cerulean, darkly, lumen, etc.
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "accent": "yellow",
    "navbar": "darkblue",
    "footer": "darkblue",
    "show_sidebar": True,
}


LOGOUT_REDIRECT_URL = 'home'  # or 'login', depending on your flow
