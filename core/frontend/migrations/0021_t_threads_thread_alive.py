# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-06 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0020_auto_20170706_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_threads',
            name='thread_alive',
            field=models.CharField(default='Y', max_length=1),
        ),
    ]