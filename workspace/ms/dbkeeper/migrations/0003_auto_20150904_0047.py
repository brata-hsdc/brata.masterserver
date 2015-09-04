# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbkeeper', '0002_auto_20150902_2340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mentor',
            old_name='mobilePhone',
            new_name='mobile_phone',
        ),
        migrations.RenameField(
            model_name='mentor',
            old_name='otherPhone',
            new_name='other_phone',
        ),
        migrations.RenameField(
            model_name='mentor',
            old_name='workPhone',
            new_name='work_phone',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='totalDuration_s',
            new_name='total_duration_s',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='totalScore',
            new_name='total_score',
        ),
    ]
