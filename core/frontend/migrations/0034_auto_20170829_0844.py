# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-29 06:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0033_auto_20170822_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_history',
            name='fail_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='t_history',
            name='pass_num',
            field=models.IntegerField(default=0),
        ),
    ]