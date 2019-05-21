# Generated by Django 2.1.1 on 2019-05-21 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontend', '0006_settings_gen_reg_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='import_his',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('imp_data', models.DateTimeField()),
                ('imp_template', models.IntegerField(default=0)),
                ('imp_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='t_assign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_tag', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('dopen', models.DateTimeField(auto_now=True)),
                ('ass_notes', models.TextField(blank=True, null=True)),
                ('id_userass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='u_ass', to=settings.AUTH_USER_MODEL)),
                ('id_userfor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='u_for', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='settings_gen',
            options={'verbose_name': 'ACCOUNT SETTINGS', 'verbose_name_plural': 'ACCOUNT SETTINGS'},
        ),
        migrations.AddField(
            model_name='t_threads',
            name='id_time',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='frontend.t_time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='t_threads',
            name='thread_runtype',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='temp_main',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AddField(
            model_name='temp_main',
            name='expected',
            field=models.TextField(blank=True, null=True, verbose_name='Expected Result'),
        ),
        migrations.AddField(
            model_name='temp_main',
            name='precond',
            field=models.TextField(blank=True, null=True, verbose_name='Preconditions'),
        ),
        migrations.AddField(
            model_name='temp_main',
            name='steps',
            field=models.TextField(blank=True, null=True, verbose_name='Steps'),
        ),
        migrations.AddField(
            model_name='temp_main',
            name='t_type',
            field=models.CharField(choices=[('Functional', 'Functional'), ('Non-Functional', 'Non-Functional')], default='Alpha', max_length=20, verbose_name='Test Type'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='settings_gen',
            name='comp_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='settings_gen',
            name='paid_plan',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Plan Selected'),
        ),
        migrations.AlterField(
            model_name='settings_gen',
            name='reg_email',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='settings_gen',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Account ID'),
        ),
        migrations.AlterField(
            model_name='settings_gen',
            name='tenant_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='System Name'),
        ),
        migrations.AlterField(
            model_name='temp_case',
            name='main_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tm_tc', to='frontend.temp_main'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='temp_pers_keywords',
            name='pers_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tk_tpk', to='frontend.temp_keywords', verbose_name='Sub Keyword'),
        ),
        migrations.AlterField(
            model_name='temp_pers_keywords',
            name='standard_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tks_tpk', to='frontend.temp_keywords', verbose_name='Keyword'),
        ),
        migrations.AddIndex(
            model_name='t_assign',
            index=models.Index(fields=['t_tag', 'id_userfor', 'id_userass'], name='frontend_t__t_tag_ab4974_idx'),
        ),
    ]
