# Generated by Django 2.0.2 on 2018-02-16 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_project_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='code',
            field=models.CharField(default=1, max_length=20, verbose_name='Project code assigned by SCW'),
            preserve_default=False,
        ),
    ]