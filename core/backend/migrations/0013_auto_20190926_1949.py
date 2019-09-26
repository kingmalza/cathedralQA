# Generated by Django 2.1.1 on 2019-09-26 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20190926_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp_main',
            name='t_doc',
            field=models.TextField(blank=True, null=True, verbose_name='Documentation'),
        ),
        migrations.AddField(
            model_name='temp_main',
            name='t_setup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_set', to='backend.temp_keywords', verbose_name='Test Setup'),
        ),
        migrations.AddField(
            model_name='temp_main',
            name='t_teardown',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_ter', to='backend.temp_keywords', verbose_name='Test Teardown'),
        ),
    ]
