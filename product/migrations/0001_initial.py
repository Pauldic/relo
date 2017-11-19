# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-19 08:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='BrandAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, default=None, null=True, upload_to=product.models.rename_and_upload, validators=[product.models.validate_file, product.models.validate_file_extension])),
                ('website', models.URLField(blank=True, default=None, null=True)),
                ('name', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=255, null=True)),
                ('title', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Brand')),
            ],
        ),
    ]