# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0007_auto_20150928_2352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pistation',
            name='pi_type',
        ),
        migrations.AddField(
            model_name='pistation',
            name='serial_num',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='pistation',
            name='url',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='pistation',
            name='station_type',
            field=models.CharField(default=b'Unknown', max_length=20, choices=[(b'Unknown', b'Unknown'), (b'RTE', b'Return to Earth (RTE)')]),
        ),
    ]
