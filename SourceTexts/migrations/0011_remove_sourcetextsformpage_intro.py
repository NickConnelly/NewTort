# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 14:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SourceTexts', '0010_sourcetextsformpage_intro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sourcetextsformpage',
            name='intro',
        ),
    ]
