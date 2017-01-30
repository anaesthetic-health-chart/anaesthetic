# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0019_auto_20170129_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='givendrug',
            name='endtime',
        ),
    ]
