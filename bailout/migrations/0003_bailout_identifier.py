# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 23:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bailout', '0002_auto_20160921_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='bailout',
            name='identifier',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
