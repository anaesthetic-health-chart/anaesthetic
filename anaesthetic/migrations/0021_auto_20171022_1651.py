# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anaesthetic', '0020_remove_givendrug_endtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergies',
            name='provisional',
            field=models.BooleanField(default=False, help_text=b'True if the allergy is only suspected. Defaults to False.', verbose_name=b'Suspected?'),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='date_of_birth',
            field=models.DateField(null=True, verbose_name=b'Date of Birth', blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='date_of_death',
            field=models.DateField(null=True, verbose_name=b'Date of Death', blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='death_indicator',
            field=models.BooleanField(default=False, help_text=b'This field will be True if the patient is deceased.'),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='hospital_number',
            field=models.CharField(help_text=b'The unique identifier for this patient at the hospital.', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='provisional',
            field=models.BooleanField(default=False, help_text=b'True if the diagnosis is provisional. Defaults to False', verbose_name=b'Provisional?'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='start_date',
            field=models.DateField(help_text=b'The date on which the patient began receiving this treatment.', null=True, blank=True),
        ),
    ]
