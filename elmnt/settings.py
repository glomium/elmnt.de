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

ADMINS = (
    ('Sebastian Braun', 'sebastian@elmnt.de'),
)

MANAGERS = ADMINS
INTERNAL_IPS = ('127.0.0.1', '85.25.139.15')
DEFAULT_FROM_EMAIL="sebastian@elmnt.de"
SERVER_EMAIL="noreply@elmnt.de"

MIGRATION_MODULES = {
    'cms': 'cms.migrations_django',
    'menus': 'menus.migrations_django',
    'filer': 'filer.migrations_django',
    'djangocms_link': 'djangocms_link.migrations_django',
    'djangocms_googlemap': 'djangocms_googlemap.migrations_django',
    'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
    'cmsplugin_filer_file': 'cmsplugin_filer_file.migrations_django',
    'cmsplugin_filer_folder': 'cmsplugin_filer_folder.migrations_django',
    'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django',
    'cmsplugin_filer_teaser': 'cmsplugin_filer_teaser.migrations_django',
    'cmsplugin_filer_video': 'cmsplugin_filer_video.migrations_django',
}

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

  # 'aldryn_search',

    'cmsplugin_bootstrap',
    'cmsplugin_cascade',
  # 'cmsplugin_slider',
  # 'cmsplugin_blueimp',
    'cmsplugin_filer_file',
    'cmsplugin_filer_image',
  # 'cmsplugin_mailform',
  # 'cmsplugin_markdown',
  # 'cmsplugin_news',

  # 'djangocms_picture',
    'djangocms_text_ckeditor',
    'djangocms_link',
    'djangocms_googlemap',


    'cms',
    'mptt',
    'menus',
    'filer',
    'sekizai',
    'reversion',
    'taggit',
    'easy_thumbnails',

    # own apps
    'groupplaner',
    'gallery',
    'elmnt',
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
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'elmnt.urls'

WSGI_APPLICATION = 'elmnt.wsgi.application'

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

# ERP =============================================================================

#ERP_DOCUMENT_ROOT = os.path.join(BASE_DIR, "documents")
#ERP_DOCUMENT_URL = '/documents/'

# CMS =========================================================================

CMS_TEMPLATES = (
    ("template_nosidebar.html", gettext("Template without sidebar")),
    ("template_sidebar.html", gettext("Template with sidebar")),
    ("template_coverpage.html", gettext("Template coverpage")),
)

LANGUAGES = [
    ('de', "Deutsch"),
    ('en', "English"),
]

CMS_PERMISSION = True


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

THUMBNAIL_BASEDIR = "pictures"
THUMBNAIL_ALIASES = {
    '': {
        'gallery_thumbnail': {
            'size': (267, 154),
            'crop': True,
            'quality': 85,
            },
        'gallery_display': {
            'size': (1140, 850),
            'quality': 95,
            },
    },
}


# LOCAL SETTINGS ==================================================================

try:
  from local_settings import *
except ImportError:
    import sys
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

    if 'runserver' in sys.argv:
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
