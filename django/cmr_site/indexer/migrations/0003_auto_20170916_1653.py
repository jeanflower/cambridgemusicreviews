# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-16 16:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexer', '0002_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='index_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='index_text',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='article',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='article',
            name='url',
            field=models.CharField(default='', max_length=400),
        ),
    ]