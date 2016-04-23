"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from .settings_default import *

ADMINS = (
    ('Sebastian Braun', 'sebastian@elmnt.de'),
)

CMSTEMPLATE_I18N_URL = True
CMSTEMPLATE_SITEMAPS['gallery'] = 'gallery.sitemaps.GallerySitemap'

MANAGERS = ADMINS
INTERNAL_IPS = ('127.0.0.1', '85.25.139.15')
DEFAULT_FROM_EMAIL="sebastian@elmnt.de"
SERVER_EMAIL="noreply@elmnt.de"

AUTH_USER_MODEL="useraccounts.User"

# Application definition
INSTALLED_APPS += [
    'useraccounts',
    # own apps
    'gallery',
    'weights',
    'elmnt',
    'cmspygments',
]

TEMPLATES[0]['OPTIONS']['context_processors'] += ['elmnt.context_processors.page_header']

# FILER =======================================================================

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
