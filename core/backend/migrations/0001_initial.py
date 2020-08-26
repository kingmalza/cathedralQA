# Generated by Django 2.1.1 on 2019-09-06 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='temp_case',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descr', models.CharField(max_length=200, verbose_name='Case description')),
                ('dt', models.DateTimeField(auto_now=True, verbose_name='Created')),
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
                ('personal', models.BooleanField(default=True, verbose_name='Personal Keyword')),
                ('dt', models.DateTimeField(auto_now=True, verbose_name='Created')),
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
                ('l_group', models.CharField(blank=True, max_length=200, null=True, verbose_name='Group')),
                ('dt', models.DateTimeField(auto_now=True, verbose_name='Created')),
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
                ('t_type', models.CharField(choices=[('Functional', 'Functional'), ('Non-Functional', 'Non-Functional')], max_length=20, verbose_name='Test Type')),
                ('precond', models.TextField(blank=True, null=True, verbose_name='Preconditions')),
                ('steps', models.TextField(blank=True, null=True, verbose_name='Steps')),
                ('expected', models.TextField(blank=True, null=True, verbose_name='Expected Result')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Note')),
                ('dt', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
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
                ('dt', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('main_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_tpk', to='backend.temp_main')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tperskey_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner')),
                ('pers_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tk_tpk', to='backend.temp_keywords', verbose_name='Sub Keyword')),
                ('standard_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tks_tpk', to='backend.temp_keywords', verbose_name='Keyword')),
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
                ('dt', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('key_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tk_ttk', to='backend.temp_keywords')),
                ('main_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_ttk', to='backend.temp_main')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ttestkey_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner')),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tc_ttk', to='backend.temp_case')),
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
                ('dt', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('main_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_tv', to='backend.temp_main')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tvar_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner')),
            ],
            options={
                'verbose_name': '3-Test Variable',
                'verbose_name_plural': '3-Test Variables',
                'ordering': ('main_id', 'v_key'),
            },
        ),
        migrations.AddField(
            model_name='temp_library',
            name='main_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_tl', to='backend.temp_main'),
        ),
        migrations.AddField(
            model_name='temp_library',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tlib_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner'),
        ),
        migrations.AddField(
            model_name='temp_case',
            name='main_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tm_tc', to='backend.temp_main'),
        ),
        migrations.AddField(
            model_name='temp_case',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tcase_owner', to=settings.AUTH_USER_MODEL, verbose_name='API Owner'),
        ),
    ]