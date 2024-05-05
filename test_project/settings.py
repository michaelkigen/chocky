"""
Django settings for test_project project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j-j)_d*m7xes3mg#$jz6jz0uinc06)j36nart$a^to1ds_59$x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'authentication.User'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'authentication',
    'rest_framework',
    'tools',
    'order',
    'courses',
    'course_order',
    'payments',

    'cloudinary_storage',
    'cloudinary',
    'django_daraja',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'test_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'test_project.wsgi.application'



SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SITE_ID = 2

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE' : [
            'profile',
            'email'
        ],
        'APP': {
            'client_id': "220876944567-b609gs9pbjrrjpaapm3mlvtft3hjhn45.apps.googleusercontent.com",
            'secret':"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"
        },
        'AUTH_PARAMS': {
            'access_type':'online',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=100),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dj1g3dh8q',
    'API_KEY': '238226323145611',
    'API_SECRET': 'vbOSg-MiYyn4-_sjCsTYP2fHvI0',
}

CORS_ALLOWED_ORIGINS = [

    "http://localhost:5173",
]

MPESA_ENVIRONMENT = 'production'
HOST_NAME=  'https://treegroup@maiyotech.com'   
CONSUMER_KEY ="Z7G6LH7b9BSOlRnwCOGNBIYZ53BZP0xZ"
CONSUMER_SECRET ="6hMTmQ09GePIzlr0"
MPESA_SHORTCODE = '7709807'
SAFARICOM_API = 'https://api.safaricom.co.ke'
MPESA_EXPRESS_SHORTCODE = '7709807'
MPESA_SHORTCODE_TYPE = 'till'
MPESA_PASSKEY = "ad1decb085daa70fe8878c7e388917735b47f4cbb6b781ad815dd7c488788fbf"
MPESA_INITIATOR_SECURITY_CREDENTIAL = 'Safaricom999!*!'
AUTH_URL = '/oauth/v1/generate?grant_type=client_credentials'
TRANSACTION_TYPE= 'CustomerBuyGoodsOnline'
TILL_NUMBER = '5737915'

PAYPAL_CLIENT_ID = 'AXhrsP_no8GZjZu_vVXw64at5ItQUqH502y2ovLfINjagVtBGjJK4_mZQ_NRHVer38j5RUMjsLSay5pp'
PAYPAL_CLIENT_SECRET = 'ELiRbt7UjajjGTZGuXoYLTIZ4gx4TwEeqeAAxUilyOs-AbIRSBCGSwXl0GiV30sMp2lIGAbqkUkHAmJC'