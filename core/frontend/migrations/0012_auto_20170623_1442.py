# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-23 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0011_auto_20170623_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='t_history',
            name='exec_user',
        ),
        migrations.RemoveField(
            model_name='t_history',
            name='id_main',
        ),
        migrations.AddField(
            model_name='t_history',
            name='test_main',
            field=models.IntegerField(default=0),
        ),
    ]
