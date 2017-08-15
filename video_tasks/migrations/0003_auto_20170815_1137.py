# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_tasks', '0002_entry_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='result',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Task Done'), (2, 'Still need to modify'), (3, 'Need Redo')], null=True),
        ),
    ]
