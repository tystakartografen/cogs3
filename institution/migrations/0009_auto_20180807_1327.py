# Generated by Django 2.0.2 on 2018-08-07 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0008_auto_20180626_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='needs_legacy_inst_id',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='institution',
            name='separate_allocation_requests',
            field=models.BooleanField(default=False),
        ),
    ]
