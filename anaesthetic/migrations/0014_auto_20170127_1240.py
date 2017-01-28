# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0013_auto_20170127_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='induction',
            name='Atracurium_dose',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='induction',
            name='Fentanul_dose',
            field=models.FloatField(default=b'100', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='induction',
            name='Propofol_dose',
            field=models.FloatField(default=b'200', null=True, blank=True),
        ),
    ]
