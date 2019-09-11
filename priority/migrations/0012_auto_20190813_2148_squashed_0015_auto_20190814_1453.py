# Generated by Django 2.2.4 on 2019-08-14 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('priority', '0012_auto_20190813_2148'), ('priority', '0013_auto_20190813_2227'), ('priority', '0014_auto_20190813_2232'), ('priority', '0015_auto_20190814_1453')]

    dependencies = [
        ('priority', '0011_remove_slurm_priority_prioritized_time'),
        ('project', '0072_auto_20190813_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlurmPriority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('account', models.CharField(max_length=20, verbose_name='Slurm account name')),
                ('attribution_points', models.IntegerField(default=50000, help_text='Calculated Attribution Points for this project', verbose_name='Attribution Points (AP)')),
                ('cpu_hours_to_date', models.IntegerField(default=0, help_text='CPU compute hours used since this project began', verbose_name='Total CPU hours to date')),
                ('gpu_hours_to_date', models.IntegerField(default=0, help_text='GPU compute hours used since this project began', verbose_name='Total GPU hours to date')),
                ('prioritised_gpu_hours', models.IntegerField(default=0, help_text='Total GPU compute hours in a prioritised state since this project began', verbose_name='Prioritised GPU hours')),
                ('prioritised_cpu_hours', models.IntegerField(default=0, help_text='Total CPU compute hours in a prioritised state since this project began', verbose_name='Prioritised CPU hours')),
                ('quality_of_service', models.IntegerField(default=0, help_text='Quality of service value for this project, to be provided to Slurm.', verbose_name='Quality of Service (QOS)')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.Project')),
            ],
        ),
        migrations.DeleteModel(
            name='slurm_priority',
        ),
    ]