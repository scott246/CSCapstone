# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 19:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GroupsApp', '0007_auto_20161207_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProjectsApp.Project'),
        ),
    ]
