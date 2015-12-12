"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

gettext = lambda s: s
BASE_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DEBUG = False

ALLOWED_HOSTS = '*'

MIGRATION_MODULES = {
#   'djangocms_link': 'djangocms_link.migrations_django',
#   'djangocms_googlemap': 'djangocms_googlemap.migrations_django',
#   'cmsplugin_filer_file': 'cmsplugin_filer_file.migrations_django',
#   'cmsplugin_filer_folder': 'cmsplugin_filer_folder.migrations_django',
#   'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django',
#   'cmsplugin_filer_teaser': 'cmsplugin_filer_teaser.migrations_django',
#   'cmsplugin_filer_video': 'cmsplugin_filer_video.migrations_django',
}

# Application definition
INSTALLED_APPS = [
    'djangocms_admin_style',

    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'bootstrap4',
    'djangocms_text_ckeditor',
    'djangocms_link',
#   'djangocms_googlemap',

    'cms',
    'menus',
    'treebeard',
    'mptt',
    'filer',
    'sekizai',
    'reversion',
    'taggit',
    'easy_thumbnails',
    'crispy_forms',
]
CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = (
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
)

ROOT_URLCONF = 'homepage.urls'

WSGI_APPLICATION = 'homepage.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'de'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            # Display fancy error pages, when DEBUG is on
            'debug': True,
            'context_processors': [
                # adds 'user' and 'perms' to request
                'django.contrib.auth.context_processors.auth',
                # if debug is true, sql_queries is added to the request
                'django.core.context_processors.debug',
                # add LANGUAGES and LANGUAGE_CODE to request
                'django.core.context_processors.i18n',
                # add MEDIA_URL to request
                'django.core.context_processors.media',
                # add STATIC_URL to request
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                # adds the request object to the request
                'django.core.context_processors.request',
                # adds messages to the request
                'django.contrib.messages.context_processors.messages',
                
                'cms.context_processors.cms_settings',
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

# CMS =========================================================================

CMS_TEMPLATES = (
    ("template_clean.html", gettext("Full width Template")),
)

LANGUAGES = [
    ('de', "Deutsch"),
]

CMS_PERMISSION = True


# FILER =======================================================================

#TEXT_SAVE_IMAGE_FUNCTION='cmsplugin_filer_image.integrations.ckeditor.create_image_plugin'

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
THUMBNAIL_QUALITY = 90


# LOCAL SETTINGS ==================================================================

try:
    from local_settings import *
except ImportError:
    import sys
    SECRET_KEY = 'just-a-dummy-key-overwrite-it-in:local_settings.py'
    SITE_ID = 1

    # Database
    # https://docs.djangoproject.com/en/dev/ref/settings/#databases
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

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# LOGGING =========================================================================
#
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

if 'DJANGO_DEBUG_TOOLBAR' in os.environ:  # pragma: no cover
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': None,
    }
