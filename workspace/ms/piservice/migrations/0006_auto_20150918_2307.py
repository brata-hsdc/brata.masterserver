# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0005_auto_20150918_1932'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pievent',
            options={'ordering': ['time'], 'managed': True},
        ),
    ]
