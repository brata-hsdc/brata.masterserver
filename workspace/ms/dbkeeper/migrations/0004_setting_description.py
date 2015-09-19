# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbkeeper', '0003_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
