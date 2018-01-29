# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import opal.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0021_auto_20171022_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnaestheticPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('Procedure_Risks', models.TextField(null=True, blank=True)),
                ('Proposed_Procedure_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ASA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dentition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FrailtyScale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Malampati',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PreOPbloods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('Hb', models.FloatField(null=True, blank=True)),
                ('Plt', models.FloatField(null=True, blank=True)),
                ('WBC', models.FloatField(null=True, blank=True)),
                ('INR', models.FloatField(null=True, blank=True)),
                ('CRP', models.FloatField(null=True, blank=True)),
                ('Urea', models.FloatField(null=True, blank=True)),
                ('Creat', models.FloatField(null=True, blank=True)),
                ('Na', models.FloatField(null=True, blank=True)),
                ('K', models.FloatField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_anaesthetic_preopbloods_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_anaesthetic_preopbloods_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PreOPvisit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('Assessment', models.TextField(null=True, blank=True)),
                ('General_Risks', models.TextField(null=True, blank=True)),
                ('AdditionalRisks', models.TextField(null=True, blank=True)),
                ('TimeSeen', models.DateTimeField(null=True, blank=True)),
                ('previous_anaesthetics_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('ASA_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('Frailty_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('Malampati_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('Dentition_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('ASA_fk', models.ForeignKey(blank=True, to='anaesthetic.ASA', null=True)),
                ('Dentition_fk', models.ForeignKey(blank=True, to='anaesthetic.Dentition', null=True)),
                ('Frailty_fk', models.ForeignKey(blank=True, to='anaesthetic.FrailtyScale', null=True)),
                ('Malampati_fk', models.ForeignKey(blank=True, to='anaesthetic.Malampati', null=True)),
                ('created_by', models.ForeignKey(related_name='created_anaesthetic_preopvisit_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PreviousAnaesthetics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProposedProcedure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Risks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='preopvisit',
            name='previous_anaesthetics_fk',
            field=models.ForeignKey(blank=True, to='anaesthetic.PreviousAnaesthetics', null=True),
        ),
        migrations.AddField(
            model_name='preopvisit',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_anaesthetic_preopvisit_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='anaestheticplan',
            name='Proposed_Procedure_fk',
            field=models.ForeignKey(blank=True, to='anaesthetic.ProposedProcedure', null=True),
        ),
        migrations.AddField(
            model_name='anaestheticplan',
            name='created_by',
            field=models.ForeignKey(related_name='created_anaesthetic_anaestheticplan_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='anaestheticplan',
            name='episode',
            field=models.ForeignKey(to='opal.Episode'),
        ),
        migrations.AddField(
            model_name='anaestheticplan',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_anaesthetic_anaestheticplan_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
