# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0016_t_schedsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_history',
            name='thread_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
