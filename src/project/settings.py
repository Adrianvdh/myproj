import os
import environ
from pathlib import Path
from pkg_resources import get_distribution
from redis import BlockingConnectionPool

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = env('SECRET_KEY', default='hd1n-(j+2vkz6dns41u6o+%_%wn0)9==%(=$-ga%uz*aefa(&f')

DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[''])


# Get distribution version used for Django cache keys
# https://docs.djangoproject.com/en/3.2/ref/settings/#version
# e.g. value: '0.1.dev2+ge8740cb.d20211016'
VERSION = env('VERSION', default=get_distribution('myproj').version)

# Application definition

INSTALLED_APPS = [
    'project',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'huey.contrib.djhuey',
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

ROOT_URLCONF = 'project.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DB_NAME = env('DB_NAME', default='myproj')  # Also use as key prefix for cache
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'HOST': env('DB_HOST', default=''),
        'PORT': env('DB_PORT', default='5432'),
        'USER': env('DB_USER', default=''),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'ATOMIC_REQUESTS': True,
    }
}


REDIS_URL = env('REDIS_URL', default='redis://localhost:6379/')
REDIS_CACHE_URL = env('REDIS_CACHE_URL', default=REDIS_URL + '0')
REDIS_QUEUE_URL = env('REDIS_QUEUE_URL', default=REDIS_URL + '1')

# Redis cache backend
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # https://docs.djangoproject.com/en/3.2/topics/cache/#cache-arguments
        'LOCATION': REDIS_CACHE_URL,
        'KEY_PREFIX': DB_NAME,
        'VERSION': VERSION
    }
}

# -----------------------------------------------------------------------------
# Huey task queue
# see: http://huey.readthedocs.io/en/latest/django.html
# -----------------------------------------------------------------------------
HUEY = {
    'name': DB_NAME,
    'immediate': False,  # run without queue in dev/test
    'results': False,
    'connection': {'connection_pool': BlockingConnectionPool.from_url(REDIS_QUEUE_URL)}
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# ------------------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'DENY'


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# ------------------------------------------------------------------------------
# Static files
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = env('STATIC_ROOT', default=os.path.join(BASE_DIR, 'static_root'))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = env('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media_root'))


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
