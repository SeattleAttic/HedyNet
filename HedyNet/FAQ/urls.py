from django.conf.urls import patterns, include, url

from .views import FAQSectionListView, FAQSectionDetailView, FAQItemDetailView

urlpatterns = patterns('',
    url(r'^$', FAQSectionListView.as_view(), name="faqsection-list"),
    url(r'^section/(?P<slug>[-\w]+)$', FAQSectionDetailView.as_view(),
        name="faqsection-detail"),
    url(r'^section/(?P<section_slug>[-\w]+)/faq/(?P<faq_slug>[-\w]+)$',
        FAQItemDetailView.as_view(), name="faqitem-detail"),
)

