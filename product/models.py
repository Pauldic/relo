from uuid import uuid4

import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.urls import reverse


class Brand(models.Model):
    name = models.CharField(max_length=64)

    @property
    def slugify(self):
        return "%s%d" % (settings.SLOG_PREFIX, (settings.SLOG_VALUE + self.id))

    def __str__(self):
        return self.name


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


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.zip', '.jpj', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Allowed files are .pdf, .zip, .jpj, .png')


def validate_file(file_obj):
    mb_limit = 50.0
    if file_obj.file.size > mb_limit*1024*1024:
        raise ValidationError('File size is larger than the allowed Limit 50mb')


class BrandAccount(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    file = models.FileField(upload_to=rename_and_upload, validators=[validate_file, validate_file_extension], blank=True, null=True, default=None)
    website = models.URLField(blank=True, null=True, default=None)
    name = models.CharField(max_length=256, blank=True, null=True, default=None)
    email = models.EmailField(max_length=255, blank=True, null=True, default=None)
    title = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return self.brand.name if self.name is None else "{} ({})".format(self.brand.name, self.name)

    def get_absolute_url(self):
        return reverse('core:upload-new',)

    @property
    def slugify(self):
        return "%s%d" % (settings.SLOG_PREFIX, (settings.SLOG_VALUE + self.id))

            # def save(self, *args, **kwargs):
    #     self.slug = self.file.name
    #     super(BrandAccount, self).save(*args, **kwargs)
    #
    # def delete(self, *args, **kwargs):
    #     """delete -- Remove to leave file."""
    #     self.file.delete(False)
    #     super(BrandAccount, self).delete(*args, **kwargs)
