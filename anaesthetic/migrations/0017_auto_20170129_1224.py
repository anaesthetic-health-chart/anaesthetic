# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0016_auto_20170127_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnaestheticDrug',
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
            name='AnaestheticDrugType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='givendrug',
            name='drug_name',
        ),
        migrations.RemoveField(
            model_name='givendrug',
            name='drug_type',
        ),
        migrations.AddField(
            model_name='givendrug',
            name='drug_name_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='givendrug',
            name='drug_type_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='givendrug',
            name='drug_name_fk',
            field=models.ForeignKey(blank=True, to='anaesthetic.AnaestheticDrug', null=True),
        ),
        migrations.AddField(
            model_name='givendrug',
            name='drug_type_fk',
            field=models.ForeignKey(blank=True, to='anaesthetic.AnaestheticDrugType', null=True),
        ),
    ]
