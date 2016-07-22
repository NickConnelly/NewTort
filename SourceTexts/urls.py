from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin

from search import views as search_views
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^new/',views.post_new, name='post_new'),
    url(r'^(?P<pk>\d+)/delete/', views.post_delete, name='post_delete'),
    url(r'^(?P<pk>\d+)/FL/', views.frequency_list, name='show_frequency_list')
]

#might need to change the directory location of the add url
"""
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
