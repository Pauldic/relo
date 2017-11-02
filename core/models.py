from uuid import uuid4

import os
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


def rename_and_upload(instance, filename):
    """
    Can rename or save the to a location of choice on the file system
    :param instance:
    :param filename:
    :return:
    """
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join('hell/deep', filename)


class RetailerAccount(models.Model):
    sChain = models.CharField(_('Name'), max_length=255, blank=False, null=False)
    sBanner_name = models.CharField(_('Banner Name'), max_length=255, blank=True, null=True, default=None)
    sLogo = models.ImageField(_('Logo'), upload_to=rename_and_upload, blank=True, null=True, default=None)
    sTypes = models.ManyToManyField('Type', verbose_name="Types", default=None, blank=True)

    def __str__(self):
        return self.sChain

    @property
    def logo_url(self):
        if self.sLogo and hasattr(self.sLogo, 'url'):
            return self.sLogo.url
        else:
            return "http://via.placeholder.com/50x50"

    @property
    def slugify(self):
        return "%s%d" % (settings.SLOG_PREFIX, (settings.SLOG_VALUE + self.id))


class StoreAccount(models.Model):
    sChain = models.ForeignKey(RetailerAccount, verbose_name="Retailer",)
    sAddOne = models.CharField(_('Add One'), max_length=255)
    sCity = models.CharField(_('City'), max_length=255)
    sState = models.CharField(_('State'), max_length=100)
    sZip = models.IntegerField(_('Zip'),)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    sPhoneOne = models.CharField(_('Phone Number'), validators=[phone_regex], max_length=100)  # validators should be a list

    @property
    def retailer_account(self):
        return RetailerAccount.objects.get(pk=self.retailer_detail_id)

    @property
    def slugify(self):
        return "%s%d" % (settings.SLOG_PREFIX, (settings.SLOG_VALUE + self.id))

    def __str__(self):
        return "%s Store" % self.sChain


class Type(models.Model):
    sType = models.CharField(_('Type'), max_length=255)

    @property
    def slugify(self):
        return "%s%d" % (settings.SLOG_PREFIX, (settings.SLOG_VALUE + self.id))

    def __str__(self):
        return self.sType

