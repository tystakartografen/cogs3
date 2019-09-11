# Generated by Django 2.0.2 on 2018-07-19 18:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0002_auto_20180515_1256'),
        ('project', '0038_auto_20180717_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalProject',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Project Title')),
                ('description', models.TextField(max_length=1024, verbose_name='Project Description')),
                ('legacy_hpcw_id', models.CharField(blank=True, help_text='Project legacy ID from HPC Wales', max_length=50, verbose_name='Legacy HPC Wales ID')),
                ('legacy_arcca_id', models.CharField(blank=True, help_text='Project legacy ID ARCCA', max_length=50, verbose_name='Legacy ARCCA ID')),
                ('code', models.CharField(max_length=20, verbose_name='Project code assigned by SCW')),
                ('gid_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='OpenLDAP GID Number')),
                ('institution_reference', models.CharField(blank=True, max_length=128, verbose_name='Owning institution project reference')),
                ('department', models.CharField(blank=True, max_length=128, verbose_name='Department')),
                ('pi', models.CharField(max_length=256, verbose_name="Principal Investigator's name, position and email")),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End date')),
                ('economic_user', models.BooleanField(default=False, verbose_name='Economic user')),
                ('requirements_software', models.TextField(blank=True, help_text='Software name and versions', max_length=512, verbose_name='Software Requirements')),
                ('requirements_gateways', models.TextField(blank=True, help_text='Web gateway or portal name and versions', max_length=512, verbose_name='Gateway Requirements')),
                ('requirements_training', models.TextField(blank=True, max_length=512, verbose_name='Training Requirements')),
                ('requirements_onboarding', models.TextField(blank=True, max_length=512, verbose_name='Onboarding Requirements')),
                ('allocation_rse', models.BooleanField(default=False, verbose_name='RSE available to?')),
                ('allocation_cputime', models.PositiveIntegerField(blank=True, null=True, verbose_name='CPU time allocation in hours')),
                ('allocation_memory', models.PositiveIntegerField(blank=True, null=True, verbose_name='RAM allocation in GB')),
                ('allocation_storage_home', models.PositiveIntegerField(blank=True, null=True, verbose_name='Home storage in GB')),
                ('allocation_storage_scratch', models.PositiveIntegerField(blank=True, null=True, verbose_name='Scratch storage in GB')),
                ('document', models.TextField(blank=True, max_length=100, null=True, verbose_name='Upload Supporting Documents')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Awaiting Approval'), (1, 'Approved'), (2, 'Declined'), (3, 'Revoked'), (4, 'Suspended'), (5, 'Closed')], default=0, verbose_name='Current Status')),
                ('previous_status', models.PositiveSmallIntegerField(choices=[(0, 'Awaiting Approval'), (1, 'Approved'), (2, 'Declined'), (3, 'Revoked'), (4, 'Suspended'), (5, 'Closed')], default=0, verbose_name='Previous Status')),
                ('reason_decision', models.TextField(blank=True, help_text="The reason will be emailed to the project's technical lead upon project status update.", max_length=256, verbose_name='Reason for the project status decision:')),
                ('notes', models.TextField(blank=True, help_text='Internal project notes', max_length=512, verbose_name='Notes')),
                ('created_time', models.DateTimeField(blank=True, editable=False, verbose_name='Created time')),
                ('modified_time', models.DateTimeField(blank=True, editable=False, verbose_name='Modified time')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('category', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='project.ProjectCategory')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('tech_lead', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical project',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalProjectCategory',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128)),
                ('description', models.TextField(max_length=512)),
                ('created_time', models.DateTimeField(blank=True, editable=False)),
                ('modified_time', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical project category',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalProjectSystemAllocation',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date_allocated', models.DateField()),
                ('date_unallocated', models.DateField()),
                ('created_time', models.DateTimeField(blank=True, editable=False)),
                ('modified_time', models.DateTimeField(blank=True, editable=False)),
                ('openldap_status', models.PositiveSmallIntegerField(choices=[(1, 'Active'), (2, 'Inactive')], default=1, verbose_name='OpenLDAP status')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='project.Project')),
                ('system', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='system.System')),
            ],
            options={
                'verbose_name': 'historical project system allocation',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalProjectUserMembership',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Awaiting Authorisation'), (1, 'Authorised'), (2, 'Declined'), (3, 'Revoked'), (4, 'Suspended')], default=0, verbose_name='Current Status')),
                ('previous_status', models.PositiveSmallIntegerField(choices=[(0, 'Awaiting Authorisation'), (1, 'Authorised'), (2, 'Declined'), (3, 'Revoked'), (4, 'Suspended')], default=0, verbose_name='Previous Status')),
                ('initiated_by_user', models.BooleanField(default=True, help_text='Determines who needs to approve the membership. The initating user is assumend to have approved it.', verbose_name='Initiated by User')),
                ('date_joined', models.DateField()),
                ('date_left', models.DateField(default=datetime.date(9999, 12, 31))),
                ('created_time', models.DateTimeField(blank=True, editable=False)),
                ('approved_time', models.DateField(default=datetime.date(9999, 12, 31))),
                ('modified_time', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='project.Project')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical project user membership',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
    ]
