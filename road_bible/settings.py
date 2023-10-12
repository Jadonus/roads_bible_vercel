"""
Django settings for road_bible project.

Generated by 'django-admin startproject' using Django 4.0.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&x$2rzcqf5w_jkx(zzz+u=99$(f^l^l*hw7f^wgi5cajc$92jp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["192.168.200.185", "roadsbible.vercel.app", "localhost", "192.168.207.164",
                 "www.roadsbible.com", "roads-bible-vercel-git-main-jadonus.vercel.app/", "localhost:8100"]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.me.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'jadongearhart@icloud.com'
EMAIL_HOST_PASSWORD = str(os.getenv('ipassword'))
DEFAULT_FROM_EMAIL = 'support@roadsbible.com'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'clearcache',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "accounts",
    "pwa",
    "road_bible",
    "corsheaders",
    "livereload",
]

MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'road_bible.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'road_bible.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'URL': str(os.getenv('RAILWAY_URL')),
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': str(os.getenv('RAILWAY_PASS')),
        'HOST': 'containers-us-west-101.railway.app',
        'PORT': 7763,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CORS_ALLOWED_ORIGINS = [
    "https://dashboard.roadsbible.com",
    "http://localhost:5173",
    "http://localhost:8000"
]
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '/static')
]  # Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = "https://dashboard.roadsbible.com"

PWA_SERVICE_WORKER_PATH = '/static/serviceworker.js'
LOGOUT_REDIRECT_URL = "/accounts/login"
PWA_APP_NAME = 'Roads'
PWA_APP_DESCRIPTION = "Roads is a bible memory app, built for the modern user. "
PWA_APP_THEME_COLOR = '#212529'
PWA_APP_BACKGROUND_COLOR = '#212529'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = 'https://dashboard.roadsbible.com'
PWA_APP_STATUS_BAR_COLOR = '#212529'
PWA_APP_ICONS = [
    {
        'src': 'static/roadspwa.png',

    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/roadspwa.png',
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/roadspwa.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
PWA_APP_SHORTCUTS = [
    {
        'name': 'Shortcut',
        'url': '/target',
        'description': 'Shortcut to a page in my application'
    }
]
PWA_APP_SCREENSHOTS = [
    {
        'src': '/static/roadsrmbg.png',
        'sizes': '750x1334',
        "type": "image/png"
    }
]
