from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

from payments import views

urlpatterns = patterns('',
    url(r'^subscriptions$', views.SubscriptionTemplateView.as_view(),
        name="subscriptions"),
    url(r'^subscriptions/thankyou$', views.SubscriptionThanksTemplateView.as_view(),
        name="subscriptions_thankyou"),

    url(r'^donations$', views.DonationTemplateView.as_view(),
        name="donations"),
    url(r'^donations/thankyou$', views.DonationThanksTemplateView.as_view(),
        name="donations_thankyou"),
)
