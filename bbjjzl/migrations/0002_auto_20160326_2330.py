# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbjjzl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('uid', models.IntegerField(default=0)),
                ('proPic', models.CharField(max_length=1000)),
                ('description', models.TextField()),
                ('nSong', models.IntegerField(default=0)),
                ('songList', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('artist', models.CharField(max_length=140)),
                ('vHash', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='musiclist',
            name='nSong',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='musiclist',
            name='songList',
            field=models.TextField(),
        ),
    ]