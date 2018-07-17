# Generated by Django 2.0.2 on 2018-06-20 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('project', '0036_auto_20180711_1259')
    ]

    operations = [
        migrations.CreateModel(
            name='FundingBody',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    )
                ),
            ],
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
        ),
        migrations.AlterModelOptions(
            name='attribution',
            options={'ordering': ('created_time',), 'verbose_name_plural': 'Attributions'},
        ),
        migrations.AlterModelOptions(
            name='fundingbody',
            options={'ordering': ('name',), 'verbose_name_plural': 'Funding Bodies'},
        ),
        migrations.AddField(
            model_name='fundingbody',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fundingbody',
            name='description',
            field=models.CharField(default=' ', max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fundingbody',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='fundingbody',
            name='name',
            field=models.CharField(default=' ', max_length=128, unique=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='FundingSource',
            fields=[
                ('attribution_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='funding.Attribution')),
                ('pi_email', models.CharField(max_length=128, null=True, verbose_name='PI Email')),
                ('funding_body', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='funding.FundingBody', verbose_name='Funding Body')),
                ('pi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pi', to=settings.AUTH_USER_MODEL, verbose_name='PI')),
            ],
            options={
                'verbose_name_plural': 'Funding Sources',
                'ordering': ('created_time',),
            },
            bases=('funding.attribution',),
        ),
        migrations.AddField(
            model_name='fundingsource',
            name='identifier',
            field=models.CharField(max_length=128, null=True, verbose_name='Local Institutional Identifier'),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('attribution_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='funding.Attribution')),
                ('identifier', models.CharField(max_length=128, null=True, verbose_name='Local Institutional Identifier or DOI')),
            ],
            options={
                'verbose_name_plural': 'Publications',
                'ordering': ('created_time',),
            },
            bases=('funding.attribution',),
        ),
    ]
