#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from datetime import timedelta
from math import sqrt


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        null=True,
        blank=False,
        related_name="+",
        on_delete=models.CASCADE,
    )
    height = models.DecimalField(
        _('Height'),
        max_digits=4,
        decimal_places=3,
        blank=False,
        help_text=_('Your height is used for calculating your BMI (X.XXX m)'),
    )
    dheight = models.DecimalField(
        _('delta height'),
        max_digits=4,
        decimal_places=3,
        blank=False,
        help_text=_('The error of your height is used to calculate the error of your BMI (X.XXX m)'),
    )
    bmitarget = models.DecimalField(
        _('bmi target'),
        max_digits=4,
        decimal_places=2,
        blank=False,
        help_text=_('Enter Your target BMI (XX.XX)'),
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
      return '%s' % self.user


@python_2_unicode_compatible
class Data(models.Model):
    user = models.ForeignKey(
        Profile,
        related_name="data",
    )
    date = models.DateTimeField(
        _('Date'),
        default=now,
        blank=False, 
    )
    weight = models.DecimalField(
        _('Weight'), 
        max_digits=4,
        decimal_places=1,
        blank=False,
        help_text=_('Enter your todays weight (XXX.X)'),
    )
    calc_vweight = models.FloatField(
        _('calculated weight'),
        null=True,
        blank=True,
    )
    calc_dweight = models.FloatField(
        _('calculated weight error'),
        null=True,
        blank=True,
    )
    calc_vslope = models.FloatField(
        _('calculated slope'),
        null=True,
        blank=True,
    )
    calc_dslope = models.FloatField(
        _('calculated slope error'),
        null=True,
        blank=True,
    )
    calc_vbmi = models.FloatField(
        _('calculated bmi'),
        null=True,
        blank=True,
    )
    calc_dbmi = models.FloatField(
        _('calculated bmi error'),
        null=True,
        blank=True,
    )
    max_weight = models.FloatField(
        _('max weight last two months'),
        null=True,
        blank=True,
    )
    min_weight = models.FloatField(
        _('min weight last two months'),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-date']
        verbose_name = _('Data')
        verbose_name_plural = _('Data')

    def __str__(self):
        return self.date.isoformat()

    def save(self, update_data=True, *args, **kwargs):
        super(Data, self).save(*args, **kwargs)
        if update_data:
            self.update_data(save=True)

    def update_data(self, save=False):

        # collect data from profile
        height = float(self.user.height)
        dheight = float(self.user.dheight)
        bmitarget = float(self.user.bmitarget)

        # create date range for 2 month stats
        date_i_m = self.date - timedelta(days=61)
        date_i_s = self.date - timedelta(days=21)

        weight_range = self.user.data.filter(
            date__range=(date_i_m, self.date)
        ).values_list("weight", flat=True)

        self.min_weight = min(weight_range)
        self.max_weight = max(weight_range)

        # create date range for calculated data
        weight_range = self.user.data.filter(
            date__range=(date_i_s, self.date)
        ).values_list("date", "weight").order_by('-date')

        # regression data: y = a + bx

        # lists 
        xl = []
        yl = []

        # sums
        sn = 0
        sx = 0
        sy = 0
        sxx = 0
        sxy = 0

        # calc sums and fill lists
        for date, weight in weight_range:
            x = (date - self.date).total_seconds() / 3600 / 24 / 7
            y = float(weight)

            xl.append(x)
            yl.append(y)

            sn += 1
            sx += x
            sy += y
            sxx += x * x
            sxy += x * y

        denominator = sn * sxx - sx * sx

        # the denominator is only zero, if there is no variance -> y = a
        if denominator == 0.:
            self.calc_vweight = self.weight
            self.calc_dweight = 0.
            self.calc_vslope = 0.
            self.calc_dslope = 0.
            self.calc_vbmi = float(self.weight) / pow(height, 2)
            self.calc_dbmi = sqrt(
                pow(
                    float(self.weight) * dheight / pow(height, 3),
                    2
                )
            )
        else:
            # y = a + bx
            a = (sy * sxx - sx * sxy) / denominator
            b = (sn * sxy - sx * sy) / denominator

            self.calc_vweight = a
            self.calc_vslope = b
            self.calc_vbmi = a / pow(height, 2)

            # calculate statistical errors
            if sn > 2:
                R = 0
                for i in range(len(xl)):
                    R += pow(yl[i] - a - xl[i] * b, 2) 
                a_error = sqrt( R * sxx / (sn-2) / denominator)
                b_error = sqrt( R * sn / (sn-2) / denominator)
            else:
                a_error = 0.
                b_error = 0.

            self.calc_dweight = a_error
            self.calc_dslope = b_error
            self.calc_dbmi = sqrt(
                pow(
                    a_error * pow(height, 2),
                    2
                ) + pow(
                    float(a) * dheight / pow(height, 3),
                    2
                )
            )

        if save:
            self.save(update_data=False)
