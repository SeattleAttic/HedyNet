from django.conf.urls import patterns, include, url

from .views import MemberDirectoryView, UserProfileDetailView, UserProfileUpdateView

urlpatterns = patterns('',
    url(r'^directory$', MemberDirectoryView.as_view(), name="memberdirectory"),
    url(r'^user/(?P<username>\w+)$', UserProfileDetailView.as_view(), name="user_profile"),
    url(r'^user/(?P<username>\w+)/edit$', UserProfileUpdateView.as_view(), name="user_profile_edit"), 
)

