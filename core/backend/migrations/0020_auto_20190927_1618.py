# Generated by Django 2.1.1 on 2019-09-27 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_auto_20190927_1232'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='temp_test_keywords',
            options={'ordering': ['my_order', 'test_id'], 'verbose_name': '4-Test Case Main Chain', 'verbose_name_plural': '4-Test Cases Main Chain'},
        ),
    ]
