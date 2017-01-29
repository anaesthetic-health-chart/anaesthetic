# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0015_auto_20170127_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='Induction_type',
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
            name='Position',
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
            model_name='induction',
            name='Induction_type_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='induction',
            name='Position_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='induction',
            name='Induction_type_fk',
            field=models.ForeignKey(blank=True, to='anaesthetic.Induction_type', null=True),
        ),
        migrations.AddField(
            model_name='induction',
            name='Position_fk',
            field=models.ForeignKey(blank=True, to='anaesthetic.Position', null=True),
        ),
    ]
