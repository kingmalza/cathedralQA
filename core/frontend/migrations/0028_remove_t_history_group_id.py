# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 07:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0027_auto_20170722_0658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='t_history',
            name='group_id',
        ),
    ]
