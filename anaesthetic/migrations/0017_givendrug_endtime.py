# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0016_auto_20170127_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='givendrug',
            name='endtime',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
