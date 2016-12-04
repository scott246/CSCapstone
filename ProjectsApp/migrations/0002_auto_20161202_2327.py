# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-02 23:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CompaniesApp', '0001_initial'),
        ('ProjectsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='company',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='CompaniesApp.Company'),
        ),
        migrations.AddField(
            model_name='project',
            name='languages',
            field=models.CharField(default=b'NON', max_length=200),
        ),
        migrations.AddField(
            model_name='project',
            name='specialty',
            field=models.CharField(default=b'0', max_length=200),
        ),
        migrations.AddField(
            model_name='project',
            name='yearsProgramming',
            field=models.CharField(default=b'0', max_length=3),
        ),
    ]