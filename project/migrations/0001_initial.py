# Generated by Django 2.0.2 on 2018-02-13 22:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Project Title')),
                ('description', models.TextField(max_length=1024, verbose_name='Project Description')),
                ('legacy_id', models.CharField(help_text='Project legacy ID from HPC Wales/ARCCA', max_length=50, verbose_name='Legacy ID')),
                ('institution_reference', models.CharField(max_length=128, verbose_name='Owning institution project reference')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('economic_user', models.BooleanField(default=False)),
                ('requirements_software', models.TextField(help_text='Software name and versions', max_length=512)),
                ('requirements_gateways', models.TextField(help_text='Gateway name and versions', max_length=512)),
                ('requirements_training', models.TextField(max_length=512)),
                ('requirements_onboarding', models.TextField(max_length=512)),
                ('allocation_rse', models.BooleanField(default=False, verbose_name='RSE available to?')),
                ('allocation_cputime', models.PositiveIntegerField(verbose_name='CPU time allocation')),
                ('allocation_storage', models.PositiveIntegerField(verbose_name='Project group storage allocation')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField(max_length=512)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Project Categories',
            },
        ),
        migrations.CreateModel(
            name='ProjectFundingSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.CharField(max_length=512)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Project Funding Sources',
            },
        ),
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Status')),
                ('description', models.CharField(max_length=512)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Project Statuses',
            },
        ),
        migrations.CreateModel(
            name='ProjectSystemAllocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_allocated', models.DateField()),
                ('date_unallocated', models.DateField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Project System Allocations',
            },
        ),
        migrations.CreateModel(
            name='ProjectUserMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Awaiting Authorisation'), (2, 'Authorised'), (3, 'Declined'), (4, 'Revoked'), (5, 'Suspended')], help_text='Authorisation status')),
                ('date_joined', models.DateField()),
                ('date_left', models.DateField(default=datetime.date(9999, 12, 31))),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
            ],
            options={
                'verbose_name_plural': 'Project User Memberships',
            },
        ),
    ]
