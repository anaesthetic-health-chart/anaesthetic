# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import opal.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0017_auto_20160509_1645'),
        ('anaesthetic', '0005_givendrug_drug_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientPhysicalAttributes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('height', models.FloatField(null=True, blank=True)),
                ('weight', models.FloatField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_anaesthetic_patientphysicalattributes_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_anaesthetic_patientphysicalattributes_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.RenameField(
            model_name='ventilators',
            old_name='mean_airway_pressure',
            new_name='peep_airway_pressure',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='height',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='weight',
        ),
        migrations.AddField(
            model_name='gases',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 15, 10, 32, 54, 824563)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ventilators',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 15, 10, 33, 14, 39944)),
            preserve_default=False,
        ),
    ]
