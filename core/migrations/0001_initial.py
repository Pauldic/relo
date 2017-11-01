# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 07:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RetailerAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sChain', models.CharField(max_length=255, verbose_name='Name')),
                ('sBanner_name', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Banner Name')),
                ('sLogo', models.ImageField(blank=True, default=None, null=True, upload_to='rename_and_upload', verbose_name='Logo')),
            ],
        ),
        migrations.CreateModel(
            name='StoreAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sAddOne', models.CharField(max_length=255, verbose_name='Add One')),
                ('sCity', models.CharField(max_length=255, verbose_name='City')),
                ('sState', models.CharField(max_length=100, verbose_name='State')),
                ('sZip', models.IntegerField(max_length=11, verbose_name='Zip')),
                ('sPhoneOne', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone Number')),
                ('sChain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.RetailerAccount', verbose_name='Retailer')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sType', models.CharField(max_length=255, verbose_name='Type')),
            ],
        ),
        migrations.AddField(
            model_name='retaileraccount',
            name='sTypes',
            field=models.ManyToManyField(blank=True, default=None, to='core.Type'),
        ),
    ]
