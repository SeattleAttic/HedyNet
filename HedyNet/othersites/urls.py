from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from othersites import views

urlpatterns = patterns('',
    url(r'^$', views.OtherSiteListView.as_view(),
        name="othersite_list"),
    url(r'^(?P<slug>[-\w]+)$', views.OtherSiteDetailView.as_view(),
        name="othersite"),
)
