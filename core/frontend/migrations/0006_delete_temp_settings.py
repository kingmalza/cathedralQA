# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-10 05:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_temp_test_keywords'),
    ]

    operations = [
        migrations.DeleteModel(
            name='temp_settings',
        ),
    ]
