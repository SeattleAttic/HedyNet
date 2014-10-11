from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^geekgirlcon$', TemplateView.as_view(template_name="promotions/geekgirlcon.html"), name="geekgirlcon"),
)
