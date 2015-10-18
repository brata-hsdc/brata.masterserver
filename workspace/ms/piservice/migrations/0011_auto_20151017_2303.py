# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0010_auto_20151006_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pievent',
            name='type',
            field=models.SmallIntegerField(default=-1, choices=[(-1, b'Unknown'), (1, b'Register'), (2, b'Check In'), (3, b'Add Organization'), (4, b'Add User'), (5, b'Add Team'), (6, b'Join'), (7, b'Leave'), (8, b'Station Status'), (9, b'Unregister'), (10, b'At Waypoint'), (11, b'Start Challenge'), (12, b'Submit'), (13, b'Register (2015)'), (14, b'At Waypoint (2015)'), (15, b'Start Challenge (2015)'), (16, b'Submit (2015)')]),
        ),
        migrations.AlterField(
            model_name='pistation',
            name='station_type',
            field=models.CharField(default=b'Unknown', max_length=20, choices=[(b'Unknown', b'Unknown'), (b'Launch', b'Launch'), (b'Dock', b'Dock'), (b'Secure', b'Secure'), (b'Return', b'Return to Earth')]),
        ),
    ]
