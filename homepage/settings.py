"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from .settings_default import *

# PROJECT_NAME = None

ADMINS = (
    ('Sebastian Braun', 'sebastian@elmnt.de'),
)

MANAGERS = ADMINS
INTERNAL_IPS = ('127.0.0.1', '85.25.139.15')
DEFAULT_FROM_EMAIL="sebastian@elmnt.de"
SERVER_EMAIL="noreply@elmnt.de"

# Application definition
INSTALLED_APPS += [
]
