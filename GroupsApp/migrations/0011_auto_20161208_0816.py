# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroupsApp', '0010_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.AddField(
            model_name='group',
            name='comment',
            field=models.CharField(default=b'', max_length=500),
        ),
    ]
