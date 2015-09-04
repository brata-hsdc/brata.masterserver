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
            name='Admin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('workPhone', models.CharField(max_length=20, blank=True)),
                ('mobilePhone', models.CharField(max_length=20, blank=True)),
                ('otherPhone', models.CharField(max_length=20, blank=True)),
                ('note', models.CharField(max_length=2000, blank=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
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
                ('pin', models.CharField(default=b'generated', max_length=20)),
                ('totalScore', models.IntegerField(default=0)),
                ('totalDuration', models.IntegerField(default=0)),
                ('school', models.ForeignKey(to='dbkeeper.School')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='mentor',
            name='school',
            field=models.ForeignKey(to='dbkeeper.School'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='teams',
            field=models.ManyToManyField(to='dbkeeper.Team'),
        ),
    ]
