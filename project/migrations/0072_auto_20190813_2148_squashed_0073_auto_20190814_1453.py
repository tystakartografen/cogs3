# Generated by Django 2.2.4 on 2019-08-14 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('project', '0072_auto_20190813_2148'), ('project', '0073_auto_20190814_1453')]

    dependencies = [
        ('project', '0071_auto_20190724_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproject',
            name='Ap',
        ),
        migrations.RemoveField(
            model_name='historicalproject',
            name='Qos',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Ap',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Qos',
        ),
        migrations.AddField(
            model_name='historicalproject',
            name='active_attribution_points',
            field=models.PositiveIntegerField(default=None, null=True, verbose_name='Attribution points at last update'),
        ),
        migrations.AddField(
            model_name='historicalproject',
            name='quality_of_service',
            field=models.PositiveIntegerField(default=None, null=True, verbose_name='Quality of Service level at last update'),
        ),
        migrations.AddField(
            model_name='project',
            name='active_attribution_points',
            field=models.PositiveIntegerField(default=None, null=True, verbose_name='Attribution points at last update'),
        ),
        migrations.AddField(
            model_name='project',
            name='quality_of_service',
            field=models.PositiveIntegerField(default=None, null=True, verbose_name='Quality of Service level at last update'),
        ),
    ]
