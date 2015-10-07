# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0008_auto_20151003_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pistation',
            name='serial_num',
            field=models.CharField(unique=True, max_length=50, blank=True),
        ),
    ]
