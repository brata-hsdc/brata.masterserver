# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0003_auto_20150911_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pistation',
            name='stationInstance',
        ),
        migrations.AddField(
            model_name='pistation',
            name='station_id',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='pievent',
            name='type',
            field=models.SmallIntegerField(default=-1, choices=[(-1, b'Unknown'), (1, b'Register'), (2, b'Check In'), (3, b'Add Organization'), (4, b'Add User'), (5, b'Add Team'), (6, b'Join'), (7, b'Leave'), (8, b'Station Status')]),
        ),
        migrations.AlterField(
            model_name='pistation',
            name='station_type',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Return to Earth (RTE)')]),
        ),
    ]
