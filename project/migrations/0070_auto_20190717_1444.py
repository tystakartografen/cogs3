# Generated by Django 2.2.2 on 2019-07-17 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0069_auto_20190710_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproject',
            name='Attribution_points',
        ),
        migrations.RemoveField(
            model_name='historicalproject',
            name='Qos',
        ),
        migrations.RemoveField(
            model_name='historicalproject',
            name='prioritized_time',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Attribution_points',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Qos',
        ),
        migrations.RemoveField(
            model_name='project',
            name='prioritized_time',
        ),
    ]
