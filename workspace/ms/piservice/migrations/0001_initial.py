# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbkeeper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PiEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField()),
                ('type', models.PositiveSmallIntegerField(default=0, choices=[(0, b'Unknown')])),
                ('data', models.CharField(max_length=2000, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PiStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=20)),
                ('ipAddress', models.CharField(max_length=16)),
                ('stationType', models.PositiveSmallIntegerField(default=0, choices=[(0, b'Unknown')])),
                ('piType', models.PositiveSmallIntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Model A'), (2, b'Model B'), (3, b'Model B+')])),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='pievent',
            name='piID',
            field=models.ForeignKey(to='piservice.PiStation'),
        ),
        migrations.AddField(
            model_name='pievent',
            name='teamID',
            field=models.ForeignKey(to='dbkeeper.Team'),
        ),
    ]
