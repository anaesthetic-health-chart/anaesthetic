# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0002_anaesthetictechnique_gases_givendrug_observation_ventilators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='givendrug',
            name='one_off',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='givendrug',
            name='started',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='givendrug',
            name='stopped',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
