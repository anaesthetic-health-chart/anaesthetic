# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0010_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gases',
            name='anaesthetic_agent',
        ),
        migrations.AddField(
            model_name='gases',
            name='expired_aa',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ventilators',
            name='tidal_volume',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
