# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-04 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0042_auto_20180404_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp_keywords',
            name='personal',
            field=models.BooleanField(default=False, verbose_name='Linked variable'),
        ),
    ]