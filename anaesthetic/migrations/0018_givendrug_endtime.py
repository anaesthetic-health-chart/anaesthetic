# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0017_auto_20170129_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='givendrug',
            name='endtime',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
