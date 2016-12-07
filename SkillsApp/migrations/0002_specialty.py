# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SkillsApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptor', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
