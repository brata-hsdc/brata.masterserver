# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2016-02-13 18:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MSUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_phone', models.CharField(blank=True, max_length=20)),
                ('mobile_phone', models.CharField(blank=True, max_length=20)),
                ('other_phone', models.CharField(blank=True, max_length=20)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, b'Unknown'), (1, b'School'), (2, b'HSDC')], default=0)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(unique=True)),
                ('value', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('pass_code', models.CharField(blank=True, max_length=50)),
                ('reg_code', models.CharField(blank=True, max_length=32)),
                ('registered', models.IntegerField(default=0)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbkeeper.Organization')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='msuser',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbkeeper.Organization'),
        ),
        migrations.AddField(
            model_name='msuser',
            name='teams',
            field=models.ManyToManyField(to='dbkeeper.Team'),
        ),
        migrations.AddField(
            model_name='msuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
