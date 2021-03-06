
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b)xb0#xtdg$-oq@il@48!@k6cpotcd0ku%f&39r^$y=8b(5o)o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['18.213.17.156', '54.72.119.195', 'localhost', '127.0.0.1', '.myaida.io']

# Application definition
SHARED_APPS = (
    'tenant_schemas',  # mandatory, should always be before any django app
    'frontend', # you must list the app where your tenant model resides in
    'backend',
    'django.contrib.contenttypes',

    # everything below here is optional
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
)

TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.admin',
    'rest_framework',
    # your tenant-specific apps
    'frontend',
    'backend',
)


INSTALLED_APPS = [
    'tenant_schemas',  # mandatory, should always be before any django app
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'frontend',
    'backend',
]

TENANT_MODEL = "frontend.Client" # app.Model

DEFAULT_FILE_STORAGE = "tenant_schemas.storage.TenantFileSystemStorage"

MIDDLEWARE = [
    'frontend.middleware.XHeaderTenantMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE_CLASSES = (
    'tenant_schemas.middleware.TenantMiddleware',
    # 'tenant_schemas.middleware.SuspiciousTenantMiddleware',
    # 'tenant_schemas.middleware.DefaultTenantMiddleware',
    # 'myproject.middleware.MyDefaultTenantMiddleware',
    #...
)

ROOT_URLCONF = 'core.urls'

#APPEND_SLASH=False

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'apptemplates.Loader',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
        ],
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


DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': '<yourdata>',
        'USER': '<yourdata>',
        'PASSWORD': '<yourdata>',
        'HOST': '<yourdata>',
        'PORT': '5432',
    }
}


#Connection Parameters for aida_lic table and marketplace
LIC_PARAM = {
    'host': '<yourdata>',
    'database': 'aida_lic',
    'user': '<yourdata>',
    'password': '<yourdata>',
}

EXPORT_PARAM = {
    'host': '<yourdata>',
    'database': '<yourdata>',
    'user': '<yourdata>',
    'password': '<yourdata>',
}

#Connection parameters for sendy db
SENDY_PARAM = {
    'db_username': "<yourdata>",
    'db_password': "<yourdata>",
    'db_name': "<yourdata>",
    'db_host': "<yourdata>"
}


DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

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
STRIPE_KEY = '<your key here>'
PROD149_KEY = '<your key here>'

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
EMAIL_HOST = '<yourdata>'
EMAIL_PORT = 587
EMAIL_FROM = 'account@myaida.io'
DEFAULT_FROM_EMAIL='account@myaida.io'
EMAIL_HOST_USER = '<yourdata>'
EMAIL_HOST_PASSWORD = '<yourdata>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
