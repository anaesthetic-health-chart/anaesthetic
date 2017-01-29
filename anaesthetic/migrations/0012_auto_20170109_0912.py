# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0025_merge'),
        ('anaesthetic', '0011_auto_20160821_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='airway',
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
            name='CormackLehane',
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
            name='Induction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('Size', models.FloatField(null=True, blank=True)),
                ('Description', models.TextField(null=True, blank=True)),
                ('MaskVent_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('Airway_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('CLview_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('Airway_fk', models.ForeignKey(blank=True, to='anaesthetic.airway', null=True)),
                ('CLview_fk', models.ForeignKey(blank=True, to='anaesthetic.CormackLehane', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MaskVent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='demographics',
            name='gp_practice_code',
            field=models.CharField(max_length=20, null=True, verbose_name=b'GP Practice Code', blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='nhs_number',
            field=models.CharField(max_length=255, null=True, verbose_name=b'NHS Number', blank=True),
        ),
        migrations.AddField(
            model_name='induction',
            name='MaskVent_fk',
            field=models.ForeignKey(blank=True, to='anaesthetic.MaskVent', null=True),
        ),
        migrations.AddField(
            model_name='induction',
            name='created_by',
            field=models.ForeignKey(related_name='created_anaesthetic_induction_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='induction',
            name='episode',
            field=models.ForeignKey(to='opal.Episode'),
        ),
        migrations.AddField(
            model_name='induction',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_anaesthetic_induction_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
