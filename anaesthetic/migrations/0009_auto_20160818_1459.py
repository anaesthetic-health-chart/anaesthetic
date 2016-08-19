# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0008_auto_20160818_1419'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anaesthetictechnique',
            old_name='induction',
            new_name='Description',
        ),
        migrations.RenameField(
            model_name='anaesthetictechnique',
            old_name='maintenance',
            new_name='Title',
        ),
        migrations.AddField(
            model_name='anaesthetictechnique',
            name='datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
