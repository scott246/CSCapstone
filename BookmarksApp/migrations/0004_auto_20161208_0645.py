# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 06:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BookmarksApp', '0003_auto_20161208_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='project',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='ProjectsApp.Project'),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
