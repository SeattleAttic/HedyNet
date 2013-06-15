from django.conf.urls import patterns, include, url

from .views import MemberDirectoryView

urlpatterns = patterns('',
    url(r'^directory$', MemberDirectoryView.as_view(), name="memberdirectory"),
)

