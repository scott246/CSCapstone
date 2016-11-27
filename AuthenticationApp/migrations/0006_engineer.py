# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 06:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0005_professor_university'),
    ]

    operations = [
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('alma_mater', models.CharField(blank=True, max_length=120, null=True)),
                ('about', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
    ]