# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-04 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0050_remove_temp_pers_keywords_variable_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='dfolder',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]