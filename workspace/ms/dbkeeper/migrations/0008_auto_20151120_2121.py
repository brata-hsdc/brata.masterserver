# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbkeeper', '0007_auto_20151118_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='registered',
            field=models.ForeignKey(related_name='teams', default=b'', to='piservice.PiEvent', null=True),
        ),
    ]
