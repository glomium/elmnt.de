#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings as djsettings


class Settings(object):

    PREFIX = "USERACCOUNTS"
    DEFAULTS = {
    
        # Enable login via...
        "LOGIN_EMAIL": True,
        "LOGIN_USERNAME": True,
        "LOGIN_TOKEN": False,

        # Login security
        "CACHE_PREFIX": "useraccounts",
        "INTERNAL_IPS": djsettings.INTERNAL_IPS,

        "THROTTLE_IP": True,
        "THROTTLE_IP_COUNT": 25,
        "THROTTLE_IP_INTERVAL": 5,

        "THROTTLE_USER": True,
        "THROTTLE_USER_COUNT": 5,
        "THROTTLE_USER_INTERVAL": 3,

        "THROTTLE_SIGNAL_TIMEOUT": 180,

        # Email validation
        "VALIDATION_SALT": "useraccounts.email",
        "VALIDATION_TIMEOUT": 72,

        "VALIDATION_SEND_MAIL": True,
        "VALIDATION_TEMPLATE_HTML": None,
        "VALIDATION_TEMPLATE_PLAIN": "useraccounts/email_validation.txt",
        "VALIDATION_TEMPLATE_SUBJECT": "useraccounts/email_validation.subject",

        # resolve views
        "RESOLVE_EMAIL_VALIDATE": None,
        "REDIRECT_EMAIL_CREATE": None,
        "REDIRECT_EMAIL_VALIDATE": None,
        "REDIRECT_EMAIL_UPDATE": None,
        "REDIRECT_EMAIL_DELETE": None,
        "REDIRECT_EMAIL_RESEND": None,

        # username
        "USERNAME_VALIDATORS": [
            {'NAME': 'useraccounts.validators.UsernameValidator'}
        ],
    }

    def __init__(self):
        for key, value in self.DEFAULTS.items():
            variable = "%s_%s" % (self.PREFIX, key)
            if not hasattr(djsettings, variable):
                setattr(djsettings, variable, value)
            setattr(self, key, getattr(djsettings, variable))


settings = Settings()
