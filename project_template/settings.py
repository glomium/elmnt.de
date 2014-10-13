"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
gettext = lambda s: s
BASE_DIR = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    "{{ APP }}.dev.igelware.de",
]

ADMINS = (
    ('Sebastian Braun', 'sebastian@elmnt.de'),
)
MANAGERS = ADMINS
INTERNAL_IPS = ('127.0.0.1', '85.25.139.15')
#DEFAULT_FROM_EMAIL="info@griba-kristiansen.de"
#SERVER_EMAIL="griba-noreply@igel-ware.de"
DEFAULT_FROM_EMAIL="team@igelware.de"
SERVER_EMAIL="noreply@igelware.de"

# Application definition
INSTALLED_APPS = (
    'djangocms_admin_style',

    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

  # 'cmsplugin_bootstrap',
  # 'cmsplugin_cascade',
  # 'cmsplugin_slider',
  # 'cmsplugin_blueimp',
  # 'cmsplugin_filer_file',
  # 'cmsplugin_filer_image',
  # 'cmsplugin_mailform',
  # 'cmsplugin_markdown',
  # 'cmsplugin_news',

  # 'djangocms_picture',
  # 'djangocms_text_ckeditor',
  # 'djangocms_link',
  # 'djangocms_googlemap',

    'cms',
    'mptt',
    'menus',
    'south',
    'sekizai',
    'reversion',
  # 'filer',
  # 'easy_thumbnails',
  # 'crispy_forms',
)
CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
   #'cms.middleware.language.LanguageCookieMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = '{{ APP }}.urls'

WSGI_APPLICATION = '{{ APP }}.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'de'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_ROOT = os.path.join(os.path.abspath(os.path.join(BASE_DIR, '..')), "static")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(os.path.abspath(os.path.join(BASE_DIR, '..')), "media")
MEDIA_URL = '/media/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

# CMS =========================================================================

CMS_TEMPLATES = (
  #  ("template_content.html", "Inhalt"),
)

LANGUAGES = [
    ('de', "German"),
]

CMS_PERMISSION = True

# SOUTH =======================================================================

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
    'reversion': 'reversion.south_migrations',
}

# FILER =======================================================================

#TEXT_SAVE_IMAGE_FUNCTION='cmsplugin_filer_image.integrations.ckeditor.create_image_plugin'

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    # 'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
THUMBNAIL_QUALITY = 90

# CMSPLUGIN_FILER_IMAGE_STYLE_CHOICES = ()
# CMSPLUGIN_FILER_IMAGE_DEFAUL_STYLE = None

# LOCAL SETTINGS ==================================================================

try:
  from local_settings import *
except ImportError:
    SECRET_KEY = 'just-a-dummy-key-overwrite-it-in:local_settings.py'
    SITE_ID = 1

#   Database
#   https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '%s/database.sqlite' % BASE_DIR,
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )


# LOGGING =========================================================================

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
