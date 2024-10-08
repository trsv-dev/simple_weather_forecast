import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http(s)://your_domain.com').split(', ')

SECRET_KEY = os.getenv('SECRET_KEY', 'you_need_to_set_the_secret_key')

DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1, localhost').split(', ')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'forecast.apps.ForecastConfig',
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

ROOT_URLCONF = 'weather_forecast.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'weather_forecast.wsgi.application'

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

LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'collected_static'

STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Saved cities settings
###############################################################################
#### How many last saved cities to display?
SAVED_CITIES = int(os.getenv('SAVED_CITIES', 10))

# Forecast settings
###############################################################################
#### From 0 to 16 days
DAYS_IN_FORECAST = int(os.getenv('DAYS_IN_FORECAST', 10))
#### From 1 to 24
HOURS_IN_FORECAST = int(os.getenv('HOURS_IN_FORECAST', 10))
#### GMT
GMT = os.getenv('GMT', '+03:00')

# Cities autocomplete settings
###############################################################################
#### Dadata token
DADATA_TOKEN = os.getenv('DADATA_TOKEN', 'your_dadata_token_from_env')
#### Dadata secret
DADATA_SECRET = os.getenv('DADATA_SECRET', 'your_dadata_secret_from_env')

# Retries quantity
###############################################################################
#### How many connection attempts before giving up
RETRIES_QUANTITY = int(os.getenv('RETRIES_QUANTITY', 10))

# Yandex API key
###############################################################################
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY', 'your_yandex_api_key_from_env')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'server_log_formatter': {
            'format': '%(asctime)s, %(levelname)s, %(message)s, %(name)s'
        },
    },
    'handlers': {
        'logfile': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/server.log',
            'maxBytes': 1024*1024*5,  # (5 MB)
            'backupCount': 3,
            'formatter': 'server_log_formatter'
        },
        'console': {
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django': {
            'level': 'WARNING',
            'handlers': ['console', 'logfile'],
        },
    },
}
