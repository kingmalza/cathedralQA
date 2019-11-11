"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b)xb0#xtdg$-oq@il@48!@k6cpotcd0ku%f&39r^$y=8b(5o)o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '127.0.0.1:8000', 'localhost:8000', '*', '192.168.99.100:8000']

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'adminsortable2',
    'frontend',
    'backend',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lyra1',
        'USER': 'kingmalza',
        'PASSWORD': '11235813post',
        'HOST': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}
"""

#For local use only
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}


#Connection Parameters for aida_lic table and marketplace
LIC_PARAM = {
    'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
    'database': 'aida_lic',
    'user': 'kingmalza',
    'password': '11235813post',
}


#Connection parameters for sendy db
SENDY_PARAM = {
    'db_username': "ytyNyqa",
    'db_password': "241cbfd1ad",
    'db_name': "sendy_db",
    'db_host': "lavaprojectdb.cre2avmtskuc.eu-west-1.rds.amazonaws.com"
}


EXPORT_PARAM = {
    'host': 'lyrards.cre2avmtskuc.eu-west-1.rds.amazonaws.com',
    'database': 'helium_ai',
    'user': 'kingmalza',
    'password': '11235813post',
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

#STRIPE SECRET KEY FOR TEST AND LIVE
#Test
STRIPE_KEY = 'sk_test_GTVLb2pY6oqhUghSl37OT3Fw'
PROD149_KEY = 'plan_E2zdkJ9EJvB7t4'

#Live
#STRIPE_KEY = 'sk_live_275LYRsuUDymanIlvV9B0HJp'
#PROD149_KEY = 'plan_E2papDJRjqTeWk'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATIC_ROOT = '/static/images/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = '/login/'

SESSION_COOKIE_AGE = 3000

# Email setting
EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_FROM = 'kingmalza@comunicame.it'
EMAIL_HOST_USER = 'AKIAJ6GB7RAIFEHEM3UA'
EMAIL_HOST_PASSWORD = 'Av+Lqj9TxNhbDINCMFEhyUrBsuNIFlf+d88Gnww12nXe'
