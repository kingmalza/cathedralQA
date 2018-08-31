# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-30 20:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontend', '0045_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='document_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner'),
            preserve_default=False,
        ),
    ]