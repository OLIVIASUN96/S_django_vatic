# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-07 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CITIS', '0016_auto_20180207_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hit',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hitgroup_hit', to='CITIS.HITGroup'),
        ),
    ]