# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-12 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
