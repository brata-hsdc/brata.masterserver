# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0002_auto_20150910_0052'),
        ('dbkeeper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='registered',
            field=models.ForeignKey(related_name='teams', to='piservice.PiEvent', null=True),
        ),
    ]
