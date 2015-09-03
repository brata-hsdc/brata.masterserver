# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pistation',
            name='hostname',
        ),
        migrations.RemoveField(
            model_name='pistation',
            name='ipAddress',
        ),
        migrations.AddField(
            model_name='pistation',
            name='host',
            field=models.CharField(max_length=60, blank=True),
        ),
        migrations.AddField(
            model_name='pistation',
            name='stationInstance',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pievent',
            name='data',
            field=models.TextField(blank=True),
        ),
    ]
