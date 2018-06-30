"""
Django settings for ff2k project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from decouple import config
import logging
import logstash

ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PACKAGE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir))
PROJECT_ROOT = os.path.abspath(
    os.path.join(PACKAGE_ROOT, os.pardir))

ASGI_APPLICATION = "ff2k.routing.application"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRONMENT == "dev":
    DEBUG = True
    ALLOWED_HOSTS = []
    ENVIRONMENT = "dev"
elif ENVIRONMENT == "docker_compose":
    DEBUG = True
    ALLOWED_HOSTS = []
elif ENVIRONMENT == "aws_beanstalk":
    DEBUG = False
    ALLOWED_HOSTS = []
else:
    DEBUG = False
    ALLOWED_HOSTS = ['www.ff2k.net', 'ff2k.net', 'alpha.ff2k.net']

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'ff2ksite.apps.Ff2KsiteConfig',
    'ff2kauthorsdesk.apps.Ff2KauthorsdeskConfig',
    'rest.apps.RestConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'channels',
    'rest_framework',
    'storages',
    'mailer',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_countries',
    'pinax.templates',
    'pinax.messages',
    'bootstrap4',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'csp.middleware.CSPMiddleware',
]

#CSP_DEFAULT_SRC = ("'self'",)

APPEND_SLASH = True
ROOT_URLCONF = 'ff2k.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pinax.messages.context_processors.user_messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ff2k.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

if ENVIRONMENT == "dev":

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

elif ENVIRONMENT == "docker_compose":

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': '3306',
        }
    }

elif ENVIRONMENT == "aws_beanstalk":

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }

elif ENVIRONMENT == "aws_prod":

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('AWS_DB_NAME'),
            'USER': config('AWS_DB_USER'),
            'PASSWORD': config('AWS_DB_PASSWORD'),
            'HOST': config('AWS_DB_HOST'),
            'PORT': '3306',
        }
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Authentication backends
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#specifying-authentication-backends

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if ENVIRONMENT == "docker_compose":
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
else:
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'


if ENVIRONMENT == "dev":

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

elif ENVIRONMENT == "docker_compose":

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [
                'memcached1:11211',
                'memcached2:11211',
            ]
        }
    }

else:

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

if ENVIRONMENT == "abc":
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

else:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    #AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_CUSTOM_DOMAIN = config('AWS_CLOUDFRONT_DOMAIN')
    #AWS_CLOUDFRONT_DOMAIN = config('AWS_CLOUDFRONT_DOMAIN')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_PRELOAD_METADATA = True
    AWS_IS_GZIPPED = False
    GZIP_CONTENT_TYPES = (
        'text/css',
        'application/javascript',
        'application/x-javascript',
        'text/javascript',
        'application/vnd.ms-fontobject',
        'application/font-sfnt',
        'application/font-woff',
    )

    AWS_LOCATION = 'static'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # https://github.com/django-compressor/django-compressor/issues/720
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        # causes verbose duplicate notifications in django 1.9
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    AWS_MEDIA_LOCATION = 'media'
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)

    #ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# coockie settings

if ENVIRONMENT == "docker_compose":
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_PATH = '/;HttpOnly'
    SESSION_COOKIE_SECURE = True
else:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False

# mail settings
EMAIL_BACKEND = 'mailer.backend.DbBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'mailer@ff2k.net'


# allauth settings
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = "False"
ACCOUNT_UNIQUE_EMAIL = "True"
ACCOUNT_EMAIL_REQUIRED = "True"
ACCOUNT_EMAIL_VERICIFATION = "optional"
ACCOUNT_EMAIL_CONFIRMATION_HMAC = "True"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = "True"
ACCOUNT_LOGIN_ON_PASSWORD_RESET = "True"
ACCOUNT_SESSION_REMEMBER = "True"
LOGIN_REDIRECT_URL = "/profile"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'logstash',
            'port': 5959,  # Default value: 5959
            # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
            'version': 1,
            # 'type' field in logstash message. Default value: 'logstash'.
            'message_type': 'django',
            # Fully qualified domain name. Default value: false.
            'fqdn': False,
            'tags': ['django.request'],  # list of tags. Default: None.
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'logstash'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'logstash'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
