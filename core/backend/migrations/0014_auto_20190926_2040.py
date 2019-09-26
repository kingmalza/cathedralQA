# Generated by Django 2.1.1 on 2019-09-26 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_auto_20190926_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp_library',
            name='main_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_tl', to='backend.temp_main', verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='temp_pers_keywords',
            name='main_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_tpk', to='backend.temp_main', verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='temp_variables',
            name='main_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_tv', to='backend.temp_main', verbose_name='Template'),
        ),
    ]
