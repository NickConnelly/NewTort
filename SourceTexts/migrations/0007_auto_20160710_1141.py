# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 11:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('SourceTexts', '0006_auto_20160710_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceTextsFormField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label')),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time')], max_length=16, verbose_name='field type')),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('choices', models.CharField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', max_length=512, verbose_name='choices')),
                ('default_value', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, verbose_name='default value')),
                ('help_text', models.CharField(blank=True, max_length=255, verbose_name='help text')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='sourcetextsformpage',
            old_name='submit_info',
            new_name='thank_you_text',
        ),
        migrations.RemoveField(
            model_name='sourcetextsformpage',
            name='thanks_info',
        ),
        migrations.AddField(
            model_name='sourcetextsformpage',
            name='from_language',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='sourcetextsformpage',
            name='source_text',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='sourcetextsformpage',
            name='to_language',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='sourcetextsformfield',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='SourceTexts.SourceTextsFormPage'),
        ),
    ]
