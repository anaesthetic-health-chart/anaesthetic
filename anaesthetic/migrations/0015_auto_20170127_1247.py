# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0014_auto_20170127_1240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='induction',
            old_name='Fentanul_dose',
            new_name='Fentanyl_dose',
        ),
    ]
