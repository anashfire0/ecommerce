# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-20 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketingpreference',
            name='mailchimp_subscribed',
            field=models.NullBooleanField(),
        ),
    ]
