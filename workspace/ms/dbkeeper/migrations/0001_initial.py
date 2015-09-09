# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MSUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('work_phone', models.CharField(max_length=20, blank=True)),
                ('mobile_phone', models.CharField(max_length=20, blank=True)),
                ('other_phone', models.CharField(max_length=20, blank=True)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('type', models.PositiveSmallIntegerField(default=0, choices=[(0, b'Unknown'), (1, b'School'), (2, b'HSDC')])),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(max_length=4, blank=True)),
                ('total_score', models.IntegerField(default=0)),
                ('total_duration_s', models.IntegerField(default=0)),
                ('organization', models.ForeignKey(to='dbkeeper.Organization')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='msuser',
            name='organization',
            field=models.ForeignKey(to='dbkeeper.Organization'),
        ),
        migrations.AddField(
            model_name='msuser',
            name='teams',
            field=models.ManyToManyField(to='dbkeeper.Team'),
        ),
        migrations.AddField(
            model_name='msuser',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
