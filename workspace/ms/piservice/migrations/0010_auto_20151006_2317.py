# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0009_auto_20151006_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pievent',
            name='message',
            field=models.CharField(max_length=1000, blank=True),
        ),
    ]
