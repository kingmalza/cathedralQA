# Generated by Django 2.1.1 on 2018-11-22 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_settings_gen_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings_gen',
            name='reg_email',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]