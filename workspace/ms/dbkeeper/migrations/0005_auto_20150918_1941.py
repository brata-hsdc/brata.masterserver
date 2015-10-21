# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbkeeper', '0004_setting_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='name',
            field=models.SlugField(unique=True),
        ),
    ]
