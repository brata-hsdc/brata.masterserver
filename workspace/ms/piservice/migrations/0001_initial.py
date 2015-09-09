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
                ('time', models.DateTimeField(auto_now_add=True)),
                ('type', models.SmallIntegerField(default=-1, choices=[(-1, b'Unknown'), (1, b'Register'), (2, b'Check In')])),
                ('status', models.SmallIntegerField(default=0, choices=[(-10, b'Fatal'), (-5, b'Warning'), (-1, b'Fail'), (0, b'Unknown'), (1, b'Success'), (5, b'Info'), (3, b'Detail')])),
                ('data', models.TextField(null=True, blank=True)),
                ('message', models.CharField(max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PiStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=60, blank=True)),
                ('station_type', models.PositiveSmallIntegerField(default=0, choices=[(0, b'Unknown')])),
                ('pi_type', models.PositiveSmallIntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Gen 1 Model A'), (2, b'Gen 1 Model A+'), (3, b'Gen 1 Model B'), (4, b'Gen 1 Model B+'), (5, b'Gen 2 Model B')])),
                ('stationInstance', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='pievent',
            name='pi',
            field=models.ForeignKey(to='piservice.PiStation', null=True),
        ),
        migrations.AddField(
            model_name='pievent',
            name='team',
            field=models.ForeignKey(to='dbkeeper.Team', null=True),
        ),
    ]
