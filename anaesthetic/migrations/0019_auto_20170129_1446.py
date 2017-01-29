# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0018_givendrug_endtime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='givendrug',
            old_name='rates',
            new_name='dose',
        ),
        migrations.RemoveField(
            model_name='givendrug',
            name='route',
        ),
    ]
