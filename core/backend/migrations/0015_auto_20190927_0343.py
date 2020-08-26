# Generated by Django 2.1.1 on 2019-09-27 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_auto_20190926_2040'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='suite_libs',
            options={'ordering': ('name', 'lib_name', 'status'), 'verbose_name': 'LIBRARY', 'verbose_name_plural': 'LIBRARIES'},
        ),
        migrations.RemoveField(
            model_name='suite_libs',
            name='f_lib',
        ),
        migrations.AlterField(
            model_name='suite_libs',
            name='descr',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='suite_libs',
            name='docs',
            field=models.TextField(blank=True, editable=False, null=True, verbose_name='Doc Link'),
        ),
        migrations.AlterField(
            model_name='suite_libs',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='suite_libs',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='suite_libs',
            name='status',
            field=models.CharField(default='ACTIVE', editable=False, max_length=10),
        ),
    ]