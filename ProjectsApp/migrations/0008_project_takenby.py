# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 22:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GroupsApp', '0008_auto_20161207_1918'),
        ('ProjectsApp', '0007_auto_20161207_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='takenBy',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='takenBy', to='GroupsApp.Group'),
        ),
    ]