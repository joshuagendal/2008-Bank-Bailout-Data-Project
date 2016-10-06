# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-23 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bailout', '0003_bailout_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='bailout',
            name='PAC',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bailout',
            name='identifier',
            field=models.IntegerField(),
        ),
    ]
