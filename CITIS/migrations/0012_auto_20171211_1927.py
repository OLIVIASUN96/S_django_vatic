# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CITIS', '0011_auto_20171211_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hit',
            name='hitslug',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
