# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0002_auto_20150910_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='pistation',
            name='joined',
            field=models.ForeignKey(to='piservice.PiEvent', null=True),
        ),
        migrations.AlterField(
            model_name='pievent',
            name='type',
            field=models.SmallIntegerField(default=-1, choices=[(-1, b'Unknown'), (1, b'Register'), (2, b'Check In'), (3, b'Add Organization'), (4, b'Add User'), (5, b'Add Team'), (6, b'Join')]),
        ),
    ]
