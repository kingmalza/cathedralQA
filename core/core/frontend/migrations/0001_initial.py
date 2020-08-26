# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-05 14:25
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tenant_schemas.postgresql_backend.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_url', models.CharField(max_length=128, unique=True)),
                ('schema_name', models.CharField(max_length=63, unique=True, validators=[tenant_schemas.postgresql_backend.base._check_schema_name])),
                ('name', models.CharField(max_length=100)),
                ('paid_until', models.DateField()),
                ('on_trial', models.BooleanField()),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(blank=True, upload_to='documents/')),
                ('dfolder', models.CharField(blank=True, max_length=255)),
                ('dmessage', models.CharField(blank=True, max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='settings_gen',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tenant_name', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='suite_libs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('descr', models.TextField(blank=True, null=True)),
                ('docs', models.TextField(blank=True, editable=False, null=True)),
                ('lib_name', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(default='APPROVAL', editable=False, max_length=10)),
                ('f_lib', models.FileField(blank=True, upload_to='libs/')),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'LIBRARIES',
                'verbose_name_plural': 'LIBRARIES',
                'ordering': ('name', 'lib_name', 'status'),
            },
        ),
        migrations.CreateModel(
            name='t_group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descr', models.CharField(max_length=50)),
                ('g_prior', models.IntegerField(default=1)),
                ('g_desc', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField(default=1)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tgrp_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'TEST GROUP MANAGER',
                'verbose_name_plural': 'TEST GROUP MANAGER',
                'ordering': ('descr',),
            },
        ),
        migrations.CreateModel(
            name='t_group_test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_ord', models.IntegerField(default=0)),
                ('id_grp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.t_group')),
            ],
            options={
                'verbose_name': 'TEST GROUP ITEMS',
                'verbose_name_plural': 'TEST GROUP ITEMS',
                'ordering': ('temp_ord',),
            },
        ),
        migrations.CreateModel(
            name='t_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_type', models.CharField(blank=True, max_length=5)),
                ('test_group', models.CharField(blank=True, max_length=50)),
                ('exec_data', models.DateTimeField(auto_now=True)),
                ('exec_status', models.CharField(max_length=10)),
                ('xml_result', models.TextField()),
                ('html_test', models.TextField()),
                ('var_test', models.TextField()),
                ('pid', models.CharField(blank=True, max_length=20, null=True)),
                ('pass_num', models.IntegerField(default=0)),
                ('fail_num', models.IntegerField(default=0)),
                ('sched_type', models.CharField(blank=True, max_length=50)),
                ('sched_val', models.CharField(blank=True, max_length=10)),
                ('thread_name', models.CharField(blank=True, max_length=100)),
                ('group_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.t_group')),
            ],
        ),
        migrations.CreateModel(
            name='t_proj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descr', models.CharField(max_length=50)),
                ('proj_notes', models.TextField(blank=True, null=True)),
                ('proj_actors', models.TextField(blank=True, null=True)),
                ('proj_start', models.DateTimeField(auto_now=True, null=True)),
                ('proj_stop', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tproj_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner')),
            ],
            options={
                'verbose_name': 'PROJECTS',
                'verbose_name_plural': 'PROJECTS',
                'ordering': ('descr',),
            },
        ),
        migrations.CreateModel(
            name='t_proj_route',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('route_notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '8-Projects Templates link',
                'verbose_name_plural': '8-Projects Templates link',
                'ordering': ('main_id', 'proj_id', 'route_notes'),
            },
        ),
        migrations.CreateModel(
            name='t_schedsettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sched_desc', models.CharField(max_length=20)),
                ('sched_command', models.CharField(max_length=20)),
                ('sched_note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_data', models.DateTimeField(auto_now=True)),
                ('exec_main', models.CharField(max_length=10)),
                ('exec_every', models.CharField(blank=True, max_length=10, null=True)),
                ('exec_at', models.CharField(blank=True, max_length=10, null=True)),
                ('last_exec', models.DateTimeField(auto_now=True)),
                ('active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='t_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descr', models.CharField(max_length=50)),
                ('tag_notes', models.TextField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ttags_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner')),
            ],
            options={
                'verbose_name': 'TAGS',
                'verbose_name_plural': 'TAGS',
                'ordering': ('descr',),
            },
        ),
        migrations.CreateModel(
            name='t_tags_route',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('route_notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '7-Tags for Templates',
                'verbose_name_plural': '7-Tags for Templates',
                'ordering': ('main_id', 'tag_id', 'route_notes'),
            },
        ),
        migrations.CreateModel(
            name='t_test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_id', models.CharField(max_length=30)),
                ('test_data', models.BinaryField()),
                ('test_rst', models.TextField()),
                ('test_html', models.TextField()),
                ('test_creation', models.DateTimeField(auto_now=True)),
                ('ip_addr', models.CharField(max_length=30)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='t_threads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thread_id', models.CharField(blank=True, max_length=50, null=True)),
                ('thread_main', models.CharField(blank=True, max_length=100, null=True)),
                ('thread_stag', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('thread_status', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
                ('thread_startd', models.DateTimeField(auto_now=True)),
                ('thread_stopd', models.DateTimeField(blank=True, null=True)),
                ('thread_ttype', models.CharField(blank=True, max_length=5)),
                ('thread_tgroup', models.CharField(blank=True, max_length=50)),
                ('thread_stype', models.CharField(blank=True, max_length=50)),
                ('thread_sval', models.CharField(blank=True, max_length=10)),
                ('id_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.t_history')),
            ],
        ),
        migrations.CreateModel(
            name='t_time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history_main', models.IntegerField(default=0)),
                ('elapsed_t', models.DecimalField(decimal_places=6, default=Decimal('0.0000'), max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='temp_case',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descr', models.CharField(max_length=200, verbose_name='Case description')),
            ],
            options={
                'verbose_name': '2-Test Case',
                'verbose_name_plural': '2-Test Cases',
                'ordering': ('descr',),
            },
        ),
        migrations.CreateModel(
            name='temp_keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descr', models.CharField(max_length=200, unique=True)),
                ('human', models.CharField(max_length=200, unique=True)),
                ('personal', models.BooleanField(default=False, verbose_name='Linked variable')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tkey_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner')),
            ],
            options={
                'verbose_name': 'KEYWORD',
                'verbose_name_plural': 'KEYWORDS',
                'ordering': ('descr',),
            },
        ),
        migrations.CreateModel(
            name='temp_library',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('l_type', models.CharField(max_length=50, verbose_name='Type')),
                ('l_val', models.CharField(max_length=100, verbose_name='Value')),
            ],
            options={
                'verbose_name': '4-Test Setting',
                'verbose_name_plural': '4-Test Settings',
                'ordering': ('main_id', 'l_type'),
            },
        ),
        migrations.CreateModel(
            name='temp_main',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descr', models.CharField(max_length=200, verbose_name='Description')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Note')),
                ('dt', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tmain_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner')),
            ],
            options={
                'verbose_name': '1-Main Template',
                'verbose_name_plural': '1-Main Templates',
            },
        ),
        migrations.CreateModel(
            name='temp_pers_keywords',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('variable_val', models.CharField(blank=True, max_length=250, null=True, verbose_name='Value')),
                ('main_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_tpk', to='frontend.temp_main')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tperskey_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner')),
                ('pers_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tk_tpk', to='frontend.temp_keywords')),
                ('standard_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tks_tpk', to='frontend.temp_keywords')),
            ],
            options={
                'verbose_name': '6-Keyword Link Chain',
                'verbose_name_plural': '6-Keywords Link Chain',
                'ordering': ('main_id', 'standard_id', 'pers_id'),
            },
        ),
        migrations.CreateModel(
            name='temp_test_keywords',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key_val', models.CharField(blank=True, max_length=200, null=True, verbose_name='Value')),
                ('key_group', models.CharField(blank=True, max_length=200, null=True, verbose_name='Group')),
                ('key_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tk_ttk', to='frontend.temp_keywords')),
                ('main_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_ttk', to='frontend.temp_main')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ttestkey_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner')),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tc_ttk', to='frontend.temp_case')),
            ],
            options={
                'verbose_name': '5-Test Case Main Chain',
                'verbose_name_plural': '5-Test Cases Main Chain',
                'ordering': ('main_id', 'test_id', 'key_id'),
            },
        ),
        migrations.CreateModel(
            name='temp_variables',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('v_key', models.CharField(max_length=200, verbose_name='Variable')),
                ('v_val', models.CharField(blank=True, max_length=200, null=True, verbose_name='Default Value')),
                ('main_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_tv', to='frontend.temp_main')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tvar_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner')),
            ],
            options={
                'verbose_name': '3-Test Variable',
                'verbose_name_plural': '3-Test Variables',
                'ordering': ('main_id', 'v_key'),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='temp_library',
            name='main_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_tl', to='frontend.temp_main'),
        ),
        migrations.AddField(
            model_name='temp_library',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tlib_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner'),
        ),
        migrations.AddField(
            model_name='temp_case',
            name='main_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tm_tc', to='frontend.temp_main'),
        ),
        migrations.AddField(
            model_name='temp_case',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tcase_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner'),
        ),
        migrations.AddField(
            model_name='t_tags_route',
            name='main_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.temp_main'),
        ),
        migrations.AddField(
            model_name='t_tags_route',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ttagsroute_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner'),
        ),
        migrations.AddField(
            model_name='t_tags_route',
            name='tag_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.t_tags'),
        ),
        migrations.AddField(
            model_name='t_schedule',
            name='id_test',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='frontend.t_test'),
        ),
        migrations.AddField(
            model_name='t_proj_route',
            name='main_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.temp_main'),
        ),
        migrations.AddField(
            model_name='t_proj_route',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tprojroute_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner'),
        ),
        migrations.AddField(
            model_name='t_proj_route',
            name='proj_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.t_proj'),
        ),
        migrations.AddField(
            model_name='t_history',
            name='test_main',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.temp_main'),
        ),
        migrations.AddField(
            model_name='t_history',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='t_group_test',
            name='id_temp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.temp_main'),
        ),
        migrations.AddField(
            model_name='t_group_test',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tgrptest_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner'),
        ),
        migrations.AddIndex(
            model_name='t_threads',
            index=models.Index(fields=['thread_stag', 'thread_status'], name='frontend_t__thread__77b533_idx'),
        ),
        migrations.AddIndex(
            model_name='t_history',
            index=models.Index(fields=['group_id'], name='frontend_t__group_i_498d4a_idx'),
        ),
    ]