# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-07 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bailout', '0012_auto_20161007_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bailout',
            name='vote_1',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
