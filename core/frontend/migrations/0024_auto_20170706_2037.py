# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-06 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0023_remove_t_threads_thread_alive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_threads',
            name='thread_main',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='t_threads',
            name='thread_stag',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
