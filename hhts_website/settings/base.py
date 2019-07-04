import os
from dotenv import load_dotenv

# Language settings
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SITE_ROOT = os.path.dirname(os.path.realpath(__name__))
SITE_ROOT = '/'.join(BASE_DIR.split('/')[:-1])

# Env Variables
# project_folder = os.path.expanduser(os.path.join(BASE_DIR, 'hhts_website'))
# load_dotenv(os.path.join(project_folder, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['localhost', 'saijosakaguradouri.pythonanywhere.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'email_blast.apps.EmailBlastConfig',
    'booking.apps.BookingConfig',
    'home.apps.HomeConfig',

    'crispy_forms',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Static files for production
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Extra language middleware - translations
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hhts_website.urls'

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

WSGI_APPLICATION = 'hhts_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# All langs
LANGUAGES = (
    ('en-us', _('English')),
    ('ja', _('Japanese')),
)

# Default lang
LANGUAGE_CODE = 'ja'

TIME_ZONE = 'UTC'

# DATETIME_INPUT_FORMATS = [
#     '%Y-%d-%m %H:%M'
# ]

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(SITE_ROOT, 'locale'),
)


# Media Files
# PUBLIC URL OF DIRECTORY
MEDIA_URL = '/media/'
# DJANGO STORES UPLOADED FILES HERE
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# FORM TEMPLATE
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# DATE FORMAT
DATETIME_FORMAT = '%d/%m/%y %H:%M'


# Redirect AFTER login
LOGIN_REDIRECT_URL = 'home'

# Redirect FOR login
LOGIN_URL = 'user-login'

# Reset password options
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Email Logins
EMAIL_HOST_USER = os.environ.get('GMAIL_ADDRESS')
EMAIL_HOST_PASSWORD = os.environ.get('MAIL_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('GMAIL_ADDRESS')
