# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0003_auto_20160514_1141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gases',
            old_name='expired_oxygens',
            new_name='expired_oxygen',
        ),
    ]
