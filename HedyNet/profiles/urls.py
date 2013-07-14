from django.conf.urls import patterns, include, url

from .views import MemberDirectoryView, UserProfileDetailView, UserProfileUpdateView, \
   MemberStatusListView, MemberStatusChangeCreateView, MemberStatusChangeDetailView, \
   MemberStatusChangeListView

urlpatterns = patterns('',
    url(r'^directory$', MemberDirectoryView.as_view(), name="memberdirectory"),
    url(r'^user/(?P<username>\w+)$', UserProfileDetailView.as_view(), name="user_profile"),
    url(r'^user/(?P<username>\w+)/edit$', UserProfileUpdateView.as_view(), name="user_profile_edit"),
)

urlpatterns += patterns('',
    url(r'^admin/memberstatuslist$', MemberStatusListView.as_view(), name="member_status_list_admin"),
    url(r'^admin/memberstatus/edit/(?P<username>\w+)$', MemberStatusChangeCreateView.as_view(), name="member_status_change_add"),
    url(r'^admin/memberstatuschange/(?P<username>\w+)/(?P<pk>\d+)$', MemberStatusChangeDetailView.as_view(), name="member_status_change_detail"),
    url(r'^admin/memberstatuschange/(?P<username>\w+)$', MemberStatusChangeListView.as_view(), name="member_status_change_list"),
)
