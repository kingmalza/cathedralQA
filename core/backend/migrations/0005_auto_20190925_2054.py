# Generated by Django 2.1.1 on 2019-09-25 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20190923_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp_keywords',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tkey_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner'),
        ),
    ]
