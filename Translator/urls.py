# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('Translator.translator',
    url(r'^maketranslate/$', 'maketranslate'),
)

urlpatterns += patterns('Translator.Frequency_list',
    url(r'^Frequency_list/(.*)', 'Frequency_list'),
)

urlpatterns += patterns('Translator.views',
    url(r'^list_frequency_lists/$', 'list_frequency_list'),
)

urlpatterns += patterns('Translator.Frequency_list_functions',
    url(r'^demo_text/(.*)', 'converted', name='converted'),
)
