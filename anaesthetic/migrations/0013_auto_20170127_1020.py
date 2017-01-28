# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0012_auto_20170109_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='induction',
            old_name='CLview_fk',
            new_name='CormackLehane_fk',
        ),
        migrations.RenameField(
            model_name='induction',
            old_name='CLview_ft',
            new_name='CormackLehane_ft',
        ),
    ]
