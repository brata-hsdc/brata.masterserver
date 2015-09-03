# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbkeeper', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='totalDuration',
            new_name='totalDuration_s',
        ),
        migrations.AlterField(
            model_name='mentor',
            name='note',
            field=models.TextField(blank=True),
        ),
    ]
