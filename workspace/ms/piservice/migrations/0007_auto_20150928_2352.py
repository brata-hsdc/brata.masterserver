# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0006_auto_20150918_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='pistation',
            name='last_activity',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 3, 52, 22, 335000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pievent',
            name='type',
            field=models.SmallIntegerField(default=-1, choices=[(-1, b'Unknown'), (1, b'Register'), (2, b'Check In'), (3, b'Add Organization'), (4, b'Add User'), (5, b'Add Team'), (6, b'Join'), (7, b'Leave'), (8, b'Station Status'), (9, b'Unregister')]),
        ),
    ]
