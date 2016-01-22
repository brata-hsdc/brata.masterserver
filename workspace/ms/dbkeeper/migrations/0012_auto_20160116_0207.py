# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-16 02:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbkeeper', '0011_team_rank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='dock_duration_s',
        ),
        migrations.RemoveField(
            model_name='team',
            name='dock_score',
        ),
        migrations.RemoveField(
            model_name='team',
            name='launch_duration_s',
        ),
        migrations.RemoveField(
            model_name='team',
            name='launch_score',
        ),
        migrations.RemoveField(
            model_name='team',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='team',
            name='return_duration_s',
        ),
        migrations.RemoveField(
            model_name='team',
            name='return_score',
        ),
        migrations.RemoveField(
            model_name='team',
            name='secure_duration_s',
        ),
        migrations.RemoveField(
            model_name='team',
            name='secure_score',
        ),
    ]