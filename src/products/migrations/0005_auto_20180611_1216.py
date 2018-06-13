# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-11 12:16
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20180611_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=products.models.upload_image_path, verbose_name='Image'),
        ),
    ]
