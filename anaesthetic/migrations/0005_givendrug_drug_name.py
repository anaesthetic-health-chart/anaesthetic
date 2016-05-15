# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0004_auto_20160514_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='givendrug',
            name='drug_name',
            field=models.CharField(default='drug name', max_length=255),
            preserve_default=False,
        ),
    ]
