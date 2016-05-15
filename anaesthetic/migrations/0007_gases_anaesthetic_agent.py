# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0006_auto_20160515_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='gases',
            name='anaesthetic_agent',
            field=models.CharField(default='something', max_length=255),
            preserve_default=False,
        ),
    ]
