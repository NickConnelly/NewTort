from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailforms.models import AbstractFormField, AbstractForm
from modelcluster.fields import ParentalKey
from django.template.response import TemplateResponse
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route



class Source(models.Model):
    title = models.TextField(max_length=200)
    text = models.TextField()
    from_language = models.TextField(null=True, max_length=100)
    to_language = models.TextField(null=True, max_length=100)
    translation = models.TextField(null=True)
    alignment = models.TextField(null=True)
    frequency_list_exists = models.TextField(null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title


class Freqlist(models.Model):
    #title = models.CharField(max_length=200, null=True)
    postpk = models.ForeignKey('Source', on_delete=models.CASCADE)
    source_text_string = models.TextField(null=True)
    translation_text_string = models.TextField(null=True)
    frequency = models.IntegerField(null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

class Knownlist(models.Model):
    #title = models.CharField(max_length=200)
    source_text_string = models.TextField(null=True)
    translation_text_string = models.TextField(null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

