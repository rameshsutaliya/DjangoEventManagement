import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v_ri2(+sg*-aemzs^9uriin2xhc4d(i%m8rntxlpg85qei-ydl'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['localhost','127.0.0.1','0.0.0.0',]
# Application definition
#import djcelery
#djcelery.setup_loader()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.postgres',
    'django_cleanup',
    'core',
    'event',
    'celery',
#    'djcelery',
#    'kombu.transport.django',
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

ROOT_URLCONF = 'kevent.urls'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['%s/templates/' % (PROJECT_DIR),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]
WSGI_APPLICATION = 'kevent.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
#I used the postgresql you can use any databases as per your requirement or design.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kiitevent',
        'USER': 'ramesh',
        'PASSWORD': 'secret',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

#for email-verfing login of user
AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.RemoteUserBackend',
        'django.contrib.auth.backends.ModelBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True
'''
	The mail server setting using my gmail account...
'''
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465 #it is for gmail check in your email service.
EMAIL_HOST_USER = '<email address>'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
DEFAULT_TO_MAIL='<default email>'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL='/'
LOGIN_URL='/login/'
LOGOUT_REDIRECT_URL='/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL='/_event_storage_/'
MEDIA_ROOT = os.path.join(BASE_DIR, '_event_storage_')
AUTH_USER_MODEL = 'core.User'
#AUTH_USER_MODEL = 'core.User'

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_TIMEZONE = 'Asia/Kolkata'



#for Custom made users
#AUTH_USER_MODEL = ‘your_app.UserAccountManager’
