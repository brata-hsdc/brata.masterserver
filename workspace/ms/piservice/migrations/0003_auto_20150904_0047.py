# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0002_auto_20150902_2340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pievent',
            old_name='piID',
            new_name='pi_id',
        ),
        migrations.RenameField(
            model_name='pievent',
            old_name='teamID',
            new_name='team_id',
        ),
        migrations.RenameField(
            model_name='pistation',
            old_name='stationType',
            new_name='station_type',
        ),
        migrations.RemoveField(
            model_name='pistation',
            name='piType',
        ),
        migrations.AddField(
            model_name='pievent',
            name='message',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='pievent',
            name='status',
            field=models.SmallIntegerField(default=-1, choices=[(-1, b'Unknown'), (0, b'Fail'), (1, b'Success')]),
        ),
        migrations.AddField(
            model_name='pistation',
            name='pi_type',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Gen 1 Model A'), (2, b'Gen 1 Model A+'), (3, b'Gen 1 Model B'), (4, b'Gen 1 Model B+'), (5, b'Gen 2 Model B')]),
        ),
        migrations.AlterField(
            model_name='pievent',
            name='type',
            field=models.SmallIntegerField(default=-1, choices=[(-1, b'Unknown'), (1, b'Register')]),
        ),
    ]
