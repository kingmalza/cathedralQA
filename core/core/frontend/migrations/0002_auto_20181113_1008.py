# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-13 09:08
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import frontend.models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='jra_history',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('j_tid', models.CharField(blank=True, max_length=1000)),
                ('j_issue', models.CharField(blank=True, max_length=255)),
                ('j_comment', models.TextField(blank=True, null=True)),
                ('j_file', models.BooleanField(default=True, verbose_name='Log file')),
                ('j_error', models.TextField(blank=True, null=True)),
                ('dt', models.DateTimeField(auto_now=True, verbose_name='Created')),
            ],
        ),
        migrations.CreateModel(
            name='jra_settings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('j_address', models.CharField(max_length=255, verbose_name='Jira server address')),
                ('j_user', models.CharField(blank=True, max_length=255, verbose_name='Username')),
                ('j_pass', models.CharField(blank=True, max_length=255, verbose_name='Password')),
                ('j_notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('dt', models.DateTimeField(auto_now=True, verbose_name='Created')),
            ],
            options={
                'verbose_name': 'JIRA SETTINGS',
                'verbose_name_plural': 'JIRA SETTINGS',
                'ordering': ('j_address',),
            },
        ),
        migrations.AlterModelOptions(
            name='t_proj',
            options={'ordering': ('descr',), 'verbose_name': 'PROJECTS MANAGER', 'verbose_name_plural': 'PROJECTS MANAGER'},
        ),
        migrations.AlterModelOptions(
            name='t_proj_route',
            options={'ordering': ('main_id', 'proj_id', 'route_notes'), 'verbose_name': 'PROJECT TEMPLATE LINK', 'verbose_name_plural': 'PROJECT TEMPLATE LINK'},
        ),
        migrations.AlterModelOptions(
            name='t_tags',
            options={'ordering': ('descr',), 'verbose_name': 'TAGS MANAGER', 'verbose_name_plural': 'TAGS MANAGER'},
        ),
        migrations.AlterModelOptions(
            name='t_tags_route',
            options={'ordering': ('main_id', 'tag_id', 'route_notes'), 'verbose_name': 'TAGS TEMPLATES LINK', 'verbose_name_plural': 'TAGS TEMPLATES LINK'},
        ),
        migrations.AlterModelOptions(
            name='t_time',
            options={'ordering': ('history_main',), 'verbose_name': 'RESOURCE USAGE', 'verbose_name_plural': 'RESOURCE USAGE'},
        ),
        migrations.RemoveField(
            model_name='client',
            name='paid_until',
        ),
        migrations.RemoveField(
            model_name='t_group',
            name='user_id',
        ),
        migrations.AddField(
            model_name='client',
            name='paid_feed',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5),
        ),
        migrations.AddField(
            model_name='suite_libs',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='t_group',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='t_group_test',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='t_proj',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='t_proj_route',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='t_tags',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='t_tags_route',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='temp_case',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='temp_keywords',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='temp_library',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='temp_library',
            name='l_group',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='temp_pers_keywords',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='temp_test_keywords',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='temp_variables',
            name='dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='suite_libs',
            name='f_lib',
            field=models.FileField(blank=True, upload_to='libs/', validators=[django.core.validators.FileExtensionValidator(['py']), frontend.models.validate_fsize], verbose_name='File ( .py Max 150Kb )'),
        ),
        migrations.AlterField(
            model_name='suite_libs',
            name='status',
            field=models.CharField(default='PENDING', editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='t_group',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='t_group',
            name='descr',
            field=models.CharField(max_length=50, verbose_name='Group name'),
        ),
        migrations.AlterField(
            model_name='t_group',
            name='g_desc',
            field=models.TextField(blank=True, null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='t_group',
            name='g_prior',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(1)], verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='t_group_test',
            name='id_grp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.t_group', verbose_name='Group'),
        ),
        migrations.AlterField(
            model_name='t_group_test',
            name='id_temp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.temp_main', verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='t_group_test',
            name='temp_ord',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Template order'),
        ),
        migrations.AlterField(
            model_name='temp_keywords',
            name='personal',
            field=models.BooleanField(default=True, verbose_name='Personal Keyword'),
        ),
        migrations.AddIndex(
            model_name='jra_history',
            index=models.Index(fields=['j_tid'], name='frontend_jr_j_tid_287596_idx'),
        ),
    ]
