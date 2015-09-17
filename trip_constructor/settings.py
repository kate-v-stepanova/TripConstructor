"""
Django settings for trip_constructor project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CURRENT_DIR = os.getcwd()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w=h9o_s3y4x@_0e9lnb#itdd^s1j06u%j3or3m%namof39g*()'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'trip_constructor',
    'django_countries',
    # 'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'trip_constructor.urls'

WSGI_APPLICATION = 'trip_constructor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'trip_constructor/static/'
TEMPLATE_DIR = os.path.join(BASE_DIR, 'trip_constructor/templates/')
MEDIA_ROOT = 'trip_constructor/media/'
MEDIA_URL = '/media/'


LIST_OF_COUNTRIES = {
    'DE': 'https://en.wikipedia.org/wiki/Visa_requirements_for_German_citizens',
    'RU': 'https://en.wikipedia.org/wiki/Visa_requirements_for_Russian_citizens',
    'ES': 'https://en.wikipedia.org/wiki/Visa_requirements_for_Spanish_citizens',
    'GB': 'https://en.wikipedia.org/wiki/Visa_requirements_for_British_citizens',
    'CA': 'https://en.wikipedia.org/wiki/Visa_requirements_for_Canadian_citizens',
    'JP': 'https://en.wikipedia.org/wiki/Visa_requirements_for_Japanese_citizens',
    'IN': 'https://en.wikipedia.org/wiki/Visa_requirements_for_Indian_citizens',
    'BR': 'https://en.wikipedia.org/wiki/Visa_requirements_for_Brazilian_citizens',
}
