from django.conf.urls import patterns, include, url

from profiles import views

urlpatterns = patterns('',
    url(r'^directory$',
        views.MemberDirectoryView.as_view(), name="memberdirectory"),
    url(r'^user/(?P<username>\w+)$',
        views.UserProfileDetailView.as_view(), name="user_profile"),
    url(r'^user/(?P<username>\w+)/edit$',
        views.UserProfileUpdateView.as_view(), name="user_profile_edit"),

    url(r'^user/(?P<username>\w+)/phone/(?P<pk>\d+)$',
        views.UserPhoneDetailView.as_view(), name="user_profile_phone_detail"),
    url(r'^user/(?P<username>\w+)/address/(?P<pk>\d+)$',
        views.UserAddressDetailView.as_view(), name="user_profile_address_detail"),
    url(r'^user/(?P<username>\w+)/email/(?P<pk>\d+)$',
        views.UserEmailDetailView.as_view(), name="user_profile_email_detail"),
    
    url(r'^user/(?P<username>\w+)/phone/add$',
        views.UserPhoneCreateView.as_view(), name="user_profile_phone_add"),
    url(r'^user/(?P<username>\w+)/address/add$',
        views.UserAddressCreateView.as_view(), name="user_profile_address_add"),
    url(r'^user/(?P<username>\w+)/email/add$',
        views.UserEmailCreateView.as_view(), name="user_profile_email_add"),

    url(r'^user/(?P<username>\w+)/phone/(?P<pk>\d+)/update$',
        views.UserPhoneUpdateView.as_view(), name="user_profile_phone_update"),
    url(r'^user/(?P<username>\w+)/address/(?P<pk>\d+)/update$',
        views.UserAddressUpdateView.as_view(), name="user_profile_address_update"),
    url(r'^user/(?P<username>\w+)/email/(?P<pk>\d+)/update$',
        views.UserEmailUpdateView.as_view(), name="user_profile_email_update"),

    url(r'^user/(?P<username>\w+)/phone/(?P<pk>\d+)/delete$',
        views.UserPhoneDeleteView.as_view(), name="user_profile_phone_delete"),
    url(r'^user/(?P<username>\w+)/address/(?P<pk>\d+)/delete$',
        views.UserAddressDeleteView.as_view(), name="user_profile_address_delete"),
    url(r'^user/(?P<username>\w+)/email/(?P<pk>\d+)/delete$',
        views.UserEmailDeleteView.as_view(), name="user_profile_email_delete"),
)

urlpatterns += patterns('',
    url(r'^admin/memberstatuslist$',
        views.MemberStatusListView.as_view(), name="member_status_list_admin"),
    url(r'^admin/memberstatuschange/(?P<username>\w+)/add$',
        views.MemberStatusChangeCreateView.as_view(), name="member_status_change_add"),
    url(r'^admin/memberstatuschange/(?P<username>\w+)/(?P<pk>\d+)$',
        views.MemberStatusChangeDetailView.as_view(), name="member_status_change_detail"),
    url(r'^admin/memberstatushistory/(?P<username>\w+)$',
        views.MemberStatusChangeListView.as_view(), name="member_status_change_list"),
)
