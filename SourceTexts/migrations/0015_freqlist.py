# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 22:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SourceTexts', '0014_auto_20160716_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Freqlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_text_string', models.TextField(null=True)),
                ('translation_text_string', models.TextField(null=True)),
                ('frequency', models.IntegerField(null=True)),
                ('postpk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SourceTexts.Post')),
            ],
        ),
    ]
