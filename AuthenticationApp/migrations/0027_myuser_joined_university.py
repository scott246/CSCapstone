# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-27 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0026_auto_20161127_0652'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='joined_university',
            field=models.BooleanField(default=False),
        ),
    ]
