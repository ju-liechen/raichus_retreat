import os
import sys
from pathlib import Path

import environ

# ==================================================================================================
# APP SETTINGS
# ==================================================================================================

APP_VERSION = 'v0.0.1'
MIN_PASSWORD_LENGTH = 8
LOGIN_REDIRECT = 'blog:index'
LOGOUT_REDIRECT = 'blog:index'
SEND_EMAILS = False  # When false, prints out what would have been sent

# ==================================================================================================
# ENVIRONMENT
# ==================================================================================================

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = 'django-insecure-s6f)@*urd_s08qm#l$)^3dj4dj3rfe%v6cnkf38t&ml=xbe0!0'
PRODUCTION = 'production'
STAGING = 'staging'
DEVELOPMENT = 'development'
TEST = 'test'
ENV = env('ENV', default=DEVELOPMENT)
TESTING = 'test' in sys.argv or ENV == TEST
DEBUG = ENV != PRODUCTION
CSRF_COOKIE_SECURE = ENV == PRODUCTION

# ==================================================================================================
# ROUTING
# ==================================================================================================

BASE_URL = env('BASE_URL', default='http://localhost:8000')
APPEND_SLASH = True
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='*').split(',')
ROOT_URLCONF = 'project.urls'
ASGI_APPLICATION = 'project.asgi.application'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = ENV == PRODUCTION

# ==================================================================================================
# APPS & MIDDLEWARE
# ==================================================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'django_htmx',

    'apps.user',
    'apps.bank',
    'apps.blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================================================================================================
# DATABASE
# ==================================================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DB_CONN_MAX_AGE = int(env('DB_CONN_MAX_AGE', default=30))

DATABASES = {
    'default': {
        'CONN_MAX_AGE': DB_CONN_MAX_AGE,
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='django'),
        'USER': env('DB_USER', default='postgres'),
        'PASSWORD': env('DB_PASS', default=''),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

# ==================================================================================================
# USER & AUTH
# ==================================================================================================

AUTH_USER_MODEL = 'user.User'
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

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# ==================================================================================================
# TIMEZONE & LANGUAGE
# ==================================================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==================================================================================================
# TEMPLATES & STATIC FILES
# ==================================================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project.context.app_version',
            ],
        },
    },
]

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# ==================================================================================================
# LOGGING
# ==================================================================================================

LOG_LEVEL = env('LOG_LEVEL', default='INFO' if ENV ==
                DEVELOPMENT else 'WARNING')
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    }
}

# ==================================================================================================
# REDIS
# ==================================================================================================

REDIS_HOST = env('REDIS_HOST', default='localhost')
REDIS_PORT = env('REDIS_PORT', default=6379)
REDIS_DB = env('REDIS_DB', default=0)
REDIS_URL = env(
    'REDIS_URL', default=f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')
REDIS_IS_TLS = REDIS_URL.startswith('rediss://')

# ==================================================================================================
# CACHE
# ==================================================================================================

CACHE_TIMEOUT = env('CACHE_TIMEOUT', default=60)  # In seconds
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": CACHE_TIMEOUT,
    }
}
if REDIS_IS_TLS:
    CACHES['default']['OPTIONS'] = {'ssl_cert_reqs': None}
