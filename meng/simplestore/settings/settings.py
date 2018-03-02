"""
Django settings for simplestore project.

For more information on this file, see
https://docs.djangoproject.com/en/1.10.5/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10.5/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f(c6z$=25y*8^(2g849k2hbjt-44b74j6nm2im8gg@#6^3v#%n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'simplestore.profiles',
    'easy_thumbnails',
    'filer',
    'mptt',
    'simplestore.sales',
    'crispy_forms',
    'storages',
    'rest_framework',
    'webpack_loader',
    'simplestore.products.apps.AppConfig',
    'simplestore.cart.apps.AppConfig',
    'simplestore.checkout.apps.AppConfig',
    'simplestore.api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'simplestore.urls'

WSGI_APPLICATION = 'simplestore.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecom',
        'USER': 'root',
        'PASSWORD': 'root',

        'HOST': '/Applications/MAMP/tmp/mysql/mysql.sock',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10.5/topics/i18n/

LANGUAGES = [
    ('en-us', 'English'),
    # ('cs-cz', 'Czech'),
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10.5/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ]
        },
    },
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/dev/',  # must end with slash
        'STATS_FILE': os.path.join(PROJECT_ROOT, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}

# Easy Thumbnails Settings
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

SITE_ID = 1

CMS_PERMISSION = True

AUTH_USER_MODEL = 'profiles.Profile'
LOGIN_URL = '/profiles/login/'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

FILER_DEBUG = True

# REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

EMAIL_ADMIN = 'csh950525@gmail.com'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '276561900@qq.com '
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
