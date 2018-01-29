# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0022_auto_20171025_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='anaestheticplan',
            name='Risks_fk',
            field=models.ForeignKey(blank=True, to='anaesthetic.Risks', null=True),
        ),
        migrations.AddField(
            model_name='anaestheticplan',
            name='Risks_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
    ]
