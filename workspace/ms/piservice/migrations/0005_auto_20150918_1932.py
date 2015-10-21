# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('piservice', '0004_auto_20150918_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pievent',
            name='pi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='piservice.PiStation', null=True),
        ),
        migrations.AlterField(
            model_name='pievent',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='dbkeeper.Team', null=True),
        ),
        migrations.AlterField(
            model_name='pistation',
            name='joined',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='piservice.PiEvent', null=True),
        ),
    ]
