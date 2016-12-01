# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-27 01:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0020_auto_20161126_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='univ',
            field=models.CharField(blank=True, choices=[('BSU', 'Ball State University'), ('PU', 'Purdue University'), ('ND', 'University of Notre Dame')], max_length=120, null=True),
        ),
    ]
