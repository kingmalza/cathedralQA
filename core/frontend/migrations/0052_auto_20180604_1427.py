# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-04 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0051_document_dfolder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(blank=True, upload_to='documents/'),
        ),
    ]
