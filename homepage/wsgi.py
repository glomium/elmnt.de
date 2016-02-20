"""
WSGI config

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homepage.settings")

from django.core.wsgi import get_wsgi_application

try:
    import uwsgi
    UWSGI = True
except ImportError:
    UWSGI = False


djangoapplication = get_wsgi_application()


def application(*args, **kwargs):
    response = djangoapplication(*args, **kwargs)
    if UWSGI:
        if hasattr(response, '_request'):
            request = getattr(response, '_request')
            if hasattr(request, 'user') and request.user.is_authenticated():
                uwsgi.set_logvar('django_user', str(request.user))
            else:
                uwsgi.set_logvar('django_user', '')
            uwsgi.set_logvar('django_dnt', str(getattr(request, 'DNT', None)).lower())
        else:
            uwsgi.set_logvar('django_user', '')
            uwsgi.set_logvar('django_dnt', 'null')
    return response
