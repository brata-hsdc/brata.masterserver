# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-07 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbkeeper', '0009_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='total_duration_s',
        ),
        migrations.RemoveField(
            model_name='team',
            name='total_score',
        ),
        migrations.AddField(
            model_name='team',
            name='dock_duration_s',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='dock_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='launch_duration_s',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='launch_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='return_duration_s',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='return_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='secure_duration_s',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='secure_score',
            field=models.IntegerField(default=0),
        ),
    ]