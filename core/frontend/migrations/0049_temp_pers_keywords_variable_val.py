# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-29 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0048_auto_20180430_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp_pers_keywords',
            name='variable_val',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
