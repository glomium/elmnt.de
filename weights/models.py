#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from datetime import datetime, timedelta


@python_2_unicode_compatible
class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )
    user = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        null=True, blank=False, editable=False,
        related_name="+", on_delete=models.CASCADE)
    birth = models.DateField(
        _('birthday'),
        blank=False,
        null=False,
        help_text=_('Your birthday is used to check your target-BMI'),
    )
    gender = models.CharField(
        _('gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        blank=False,
        help_text=_('Your gender is used to check yout target-BMI'),
    )
    height = models.DecimalField(
        _('height'),
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
      return self.user


class Data(models.Model):
    user = models.ForeignKey(
        Profile,
        unique_for_date="date",
        related_name="data",
    )
    date = models.DateTimeField(
        _('date'),
        default=now,
        blank=False, 
    )
    weight = models.DecimalField(
        _('weight'), 
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

    def save(self,update_data=True,*args,**kwargs):
        super(Data, self).save(*args,**kwargs)
        if update_data:
            data_save.delay(pk=self.pk)

    # get statistics for the statistic page
    def get_stats(self, profile):
        val = {
            'weight_value':   0.0,
            'weight_error':   0.0,
            'change_bool':    False,
            'change_value':   0.0,
            'change_error':   0.0,
            'bmi_value':      0.0,
            'bmi_error':      0.0,
            'predict_bool':   False,
            'target_bmi':     0.0,
            'target_weight':  0.0,
            'target_error':   0.0,
            'target_reached': False,
            'target_reach':   False,
            'target_msg':     '',
            'target_weeks':   0.0,
            'target_date':    now(),
        }

        if not isinstance(profile, Profile):
            return val

        if self.calc_vweight:
            val['weight_value'] = self.calc_vweight
            val['weight_error'] = self.calc_dweight
        else:
            val['weight_value'] = self.weight

        if self.calc_vslope:
            val['change_bool']  = True
            val['change_value'] = self.calc_vslope*7000
            val['change_error'] = self.calc_dslope*7000

        if not self.calc_vbmi:
            val['target_msg'] = _('Not enoth datapoints')
            return val

        val['bmi_value'] = self.calc_vbmi
        val['bmi_error'] = self.calc_dbmi

        val['target_bmi']    = float(profile.bmitarget)
        val['target_weight'] = float(profile.bmitarget)*pow(float(profile.height),2)
        val['target_error']  = self.calc_dbmi*pow(float(profile.height),2)

        if val['target_bmi'] < val['bmi_value'] + val['bmi_error'] and val['target_bmi'] > val['bmi_value'] - val['bmi_error']:
            val['target_reached'] = True
            return val

        if not self.calc_vslope or not self.calc_vweight:
            val['target_msg'] = _('Not enoth datapoints')
            return val
          
        if self.calc_vslope == 0 or self.calc_vslope < 0 and val['bmi_value'] < val['target_bmi'] or self.calc_vslope > 0 and val['bmi_value'] > val['target_bmi']:
            val['target_msg'] = _('Wrong trend')
            return val
          
        val['target_reach'] = True
        targetrate = (val['target_weight']-self.calc_vweight)/self.calc_vslope
        val['target_weeks'] = targetrate/7
        val['target_date']  = self.date + timedelta(days=targetrate)
        return val


class Month(models.Model):
    user = models.ForeignKey(
        Profile,
        unique_for_month="date",
        related_name="+",
    )
    date = models.DateField(
        _('date'),
        default=now,
        blank=False,
    )
    evaluate = models.BooleanField(
        _('evaluate'),
        default=False,
    )
    weight = models.FloatField(
        _('weight'),
        null=True,
        blank=True,
    )
    dweight = models.FloatField(
        _('delta weight'),
        null=True,
        blank=True,
    )
    bmi = models.FloatField(
        _('bmi'),
        null=True,
        blank=True,
    )
    dbmi = models.FloatField(
        _('delta bmi'),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-date']
        verbose_name = _('Month')
        verbose_name_plural = _('Months')

    def __unicode__(self):
        return self.date.isoformat()

    @models.permalink
    def get_absolute_url(self):
        return ('diet_statistic_month', None, {
            'year': self.date.year,
            'month': self.date.strftime('%m'),
        })

    def get_previous_month(self):
        date_ende  = datetime( self.date.year, self.date.month, 1) - timedelta(days=1)
        date_start = datetime( date_ende.year, date_ende.month, 1)
        try:
            entry = Month.objects.get(user_id=self.user_id, date__range=(date_start,date_ende))
        except Month.DoesNotExist:
            entry = None
        return entry 

    def save(self,*args,**kwargs):
        new = False
        if not self.pk:
            graph = Graph(user=self.user,pretag=self.date.strftime('%Y-%m'))
            graph.save()
        super(Month, self).save(*args,**kwargs)
        month_save.delay(self.pk)
