from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-z2i=j(%_#7vjo*(82j@9#3&_gifczx#4d5=pnxh$n^!+l^8n+%'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Payment Method
    'paypal.standard.ipn',
    # Text Editor
    'ckeditor',
    'ckeditor_uploader',
    # My Apps
    'gorkems_doner_theme',
    'gorkems_doner_shop',
    'gorkems_doner_user',
    'gorkems_doner_message',
    'gorkems_doner_admin',
]


PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = 'sb-tae4q7811147@business.example.com'


CKEDITOR_UPLOAD_PATH = "inTextPicture/"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gorkems_doner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom Context Processors For WebApp
                'gorkems_doner_theme.context_processors.get_all_user',
            ],
        },
    },
]

WSGI_APPLICATION = 'gorkems_doner.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = BASE_DIR, 'static'
# STATIC_ROOT = '/home/websites/goerkems_doener/gorkems_doner/static'


MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR/'media'
MEDIA_ROOT = '/home/websites/goerkems_doener/gorkems_doner/media'


# Login Credential
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'


# Social Login API

SOCIAL_AUTH_FACEBOOK_KEY = ''  # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = ''  # Facebook App Secret
SOCIAL_AUTH_GOOGLE_KEY = ''  # Client ID
SOCIAL_AUTH_GOOGLE_SECRET = ''  # Client Secret

# Gmail options webserver
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True


# CKEditor Configuration Settings
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar': 'full',
        'width': 'auto',
        'height': 'auto'
    }
}
