# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-30 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0046_document_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='owner',
            field=models.CharField(max_length=50),
        ),
    ]
