# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-02 08:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0049_temp_pers_keywords_variable_val'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temp_pers_keywords',
            name='variable_id',
        ),
    ]
