# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0007_gases_anaesthetic_agent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='givendrug',
            old_name='one_off',
            new_name='datetime',
        ),
        migrations.RemoveField(
            model_name='givendrug',
            name='started',
        ),
        migrations.RemoveField(
            model_name='givendrug',
            name='stopped',
        ),
    ]
