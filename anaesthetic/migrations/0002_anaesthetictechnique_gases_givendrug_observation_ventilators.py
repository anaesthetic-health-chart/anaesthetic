# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import opal.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0017_auto_20160509_1645'),
        ('anaesthetic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnaestheticTechnique',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('induction', models.TextField(null=True, blank=True)),
                ('maintenance', models.TextField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_anaesthetic_anaesthetictechnique_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_anaesthetic_anaesthetictechnique_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Gases',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('inspired_carbon_dioxide', models.FloatField(null=True, blank=True)),
                ('expired_carbon_dioxide', models.FloatField(null=True, blank=True)),
                ('inspired_oxygen', models.FloatField(null=True, blank=True)),
                ('expired_oxygens', models.FloatField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_anaesthetic_gases_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_anaesthetic_gases_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GivenDrug',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('route', models.CharField(max_length=255)),
                ('drug_type', models.CharField(max_length=255)),
                ('rates', models.CharField(max_length=255)),
                ('started', models.DateTimeField()),
                ('stopped', models.DateTimeField()),
                ('one_off', models.DateTimeField()),
                ('created_by', models.ForeignKey(related_name='created_anaesthetic_givendrug_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_anaesthetic_givendrug_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('bp_systolic', models.FloatField(null=True, blank=True)),
                ('bp_diastolic', models.FloatField(null=True, blank=True)),
                ('pulse', models.FloatField(null=True, blank=True)),
                ('resp_rate', models.FloatField(null=True, blank=True)),
                ('sp02', models.FloatField(null=True, blank=True)),
                ('temperature', models.FloatField(null=True, blank=True)),
                ('height', models.FloatField(null=True, blank=True)),
                ('weight', models.FloatField(null=True, blank=True)),
                ('datetime', models.DateTimeField()),
                ('created_by', models.ForeignKey(related_name='created_anaesthetic_observation_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_anaesthetic_observation_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Ventilators',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('mode', models.CharField(max_length=255)),
                ('peak_airway_pressure', models.FloatField(null=True, blank=True)),
                ('mean_airway_pressure', models.FloatField(null=True, blank=True)),
                ('rate', models.IntegerField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_anaesthetic_ventilators_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_anaesthetic_ventilators_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
