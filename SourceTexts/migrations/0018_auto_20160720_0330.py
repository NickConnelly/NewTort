# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SourceTexts', '0017_auto_20160717_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='title',
            field=models.TextField(max_length=200),
        ),
    ]
