import os
from pathlib import Path
import environ # type: ignore

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-t$if7u3$amts9&=q-dbvmk%p@g0$hyz3)+2-fzpy6vi@1a()-z"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
LOCAL_APPS = [
    'apps.users.apps.UsersConfig',
    'apps.affiliates.apps.AffiliatesConfig',
]

# Third party applications
THIRD_PARTY_APPS = [
    'debug_toolbar',
    'jazzmin',
]

# Installed apps
INSTALLED_APPS = [
    *THIRD_PARTY_APPS,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *LOCAL_APPS,
]

if DEBUG:
    INTERNAL_IPS = type(str('c'), (), {'__contains__': lambda *a: True})()

# middleware
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'apps' / 'users' / 'templates',BASE_DIR / 'apps' / 'affiliates' / 'templates'],
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

# WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'HOST': 'db',
        'PORT': env('DB_PORT'),
        'PASSWORD': env('DB_PASSWORD')
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'shyskov@.ru'
EMAIL_HOST_PASSWORD = 'app_password'


# Password validation
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

LOGGING = {
    'version':1,
    'disable_exiting_logger':False,
    'formatters':{
        "standard":{
            "format" : "%(asctime)s %(levelname)s %(name)s %(message)s"
        }
    },
    'handlers':{
        'console': {
            'class' : 'logging.StreamHandler',
            'formatter': "standard",
        },
        'file': {
            'class' : 'logging.FileHandler',
            'formatter': "standard",
            'filename' : "info.log"
        }
    },
    'loggers':{
        'main':{
            'handlers' : ['console', 'file'],
            'level' : 'DEBUG',
            'propagate' : True,
        },
        'affiliates':{
            'handlers' : ['console', 'file'],
            'level' : 'DEBUG',
            'propagate' : True,
        }
    }
}


# Internationalization
LANGUAGE_CODE = 'en-us'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'

JAZZMIN_SETTINGS = {
    "site_header": "Insurance administration",
}