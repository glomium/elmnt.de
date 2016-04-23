#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core import validators
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.utils.translation import ugettext_lazy as _


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                'letters, numbers ' 'and @/./+/-/_ characters.')
                ),
            ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True, editable=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class AbstractEmail(models.model):
    email = models.EmailField(_('email address'), blank=False, db_index=True)
    code = models.CharField(_('code'), max_length=32, editable=False, blank=True)

    is_primary = models.BooleanField(
        _('primary'),
        default=False,
        db_index=True,
    )
    is_visible = models.BooleanField(
        _('visible'),
        default=True,
    )
    is_valid = models.BooleanField(
        _('active'),
        default=False,
    )

    validated = models.DateTimeField(_('validated'), editable=False, null=True, blank=True)
    created = models.DateTimeField(_('created'), editable=False, auto_now_add=True)
    updated = models.DateTimeField(_('updated'), editable=False, auto_now=True)

    class Meta:
        verbose_name = _('Email')
        verbose_name_plural = _('Emails')
        abstract = True


class User(AbstractUser):
    pass


class Email(AbstractEmail):
    pass
