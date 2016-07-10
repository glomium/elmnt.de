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
PROJECT_NAME = os.environ.get('PROJECT_NAME', None)

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
    'useraccounts',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'bootstrap4',
    'mailform',
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
    'homepage.middleware.PrivacyMiddleware',
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

                # adds the DoNotTrack as variable to the context
                'homepage.context_processors.dnt',

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

FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT,
                'base_url': MEDIA_URL,
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
            'UPLOAD_TO_PREFIX': 'filer',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT,
                'base_url': MEDIA_URL,
            },
            'THUMBNAIL_OPTIONS': {
                'base_dir': 'thumbnails',
            },
        },
    },
}

#TEXT_SAVE_IMAGE_FUNCTION='cmsplugin_filer_image.integrations.ckeditor.create_image_plugin'

THUMBNAIL_PROCESSORS = (

    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    # 'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
    'easy_thumbnails.processors.background',
)

THUMBNAIL_QUALITY = 90


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
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
             'level': 'DEBUG',
             'filters': ['require_debug_true'],
             'class': 'logging.StreamHandler',
             'formatter': 'verbose',
         },
        'logstash':{
             'level': 'INFO',
             'filters': ['require_debug_false'],
             'class': 'logstash.TCPLogstashHandler',
             'host': '127.0.0.1',
             'port': 5959,
             'version': 1,
             'message_type': 'django',
             'fqdn': False,
             'tags': ["cmstemplate", os.path.basename(BASE_DIR)]
         },
    },
    'root': {
        'handlers': ['logstash'],
        'level': 'INFO',
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# CMS TEMPLATE ====================================================================

CMSTEMPLATE_SITEMAPS = {
    'cmspages': 'cms.sitemaps.CMSSitemap',
}


# LOCAL SETTINGS ==================================================================

try:
    from local_settings import *
except ImportError:
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


# SESSION =========================================================================

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
if PROJECT_NAME and 'MEMCACHED_PORT_11211_TCP_ADDR' in os.environ:  # pragma: no cover
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
           'KEY_PREFIX': PROJECT_NAME,
           'LOCATION': '%s:%s' % (
                os.environ.get('MEMCACHED_PORT_11211_TCP_ADDR'),
                os.environ.get('MEMCACHED_PORT_11211_TCP_PORT', 11211),
           ),
        },
    }

# DEBUG TOOLBAR ===================================================================

if 'DJANGO_DEBUG_TOOLBAR' in os.environ and os.environ['DJANGO_DEBUG_TOOLBAR']:  # pragma: no cover
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': None,
    }
else:
    MIDDLEWARE_CLASSES = (
        'cms.middleware.utils.ApphookReloadMiddleware',
    ) + MIDDLEWARE_CLASSES
