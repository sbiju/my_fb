# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-28 06:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20160723_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='active',
        ),
    ]
