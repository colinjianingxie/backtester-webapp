"""
Django settings for codepass project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import sys
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(
    0, os.path.join(BASE_DIR, "apps")
)  # Allows for apps folder to be utilized

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p@p#k_hlr34z7%qiar(4qk3czz+dlapz7m!)&5(m#rai1fn@yz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    "main",
    "api",
    "home",
    "securities_master",
    "securities_scraper",
    "oauth",
    "dashboard",
    "rest_framework",
    "utils",
    'corsheaders',
    'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
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
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates/"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "utils.helper.load_template_variables.load_all_symbols",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'securities_master',
        'USER': 'postgres',
        'PASSWORD': 'WANG',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
AUTH_USER_MODEL = "oauth.Account"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = ['%Y-%m-%d']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    Path(BASE_DIR).joinpath("static")
]

LOGIN_URL = "/oauth/accounts/login"  # Base Redirection
LOGIN_REDIRECT_URL = (
    "/dashboard/login_redirect_success"  # Redirect to home URL after login
)
LOGOUT_REDIRECT_URL = LOGIN_URL


EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"  # Default Email backend:
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
