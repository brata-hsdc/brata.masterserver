# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbkeeper', '0006_auto_20150920_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='registered',
            field=models.ForeignKey(related_name='teams', default=b'', blank=True, to='piservice.PiEvent'),
        ),
    ]
