# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbkeeper', '0005_auto_20150918_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='code',
        ),
        migrations.AddField(
            model_name='team',
            name='pass_code',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='reg_code',
            field=models.CharField(max_length=32, blank=True),
        ),
    ]
