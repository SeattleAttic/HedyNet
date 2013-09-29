from __future__ import unicode_literals

from django.views.generic import ListView, DetailView

from othersites import models

class OtherSiteListView(ListView):
    
    model = models.OtherSite
    context_object_name = "othersite_list"

    def get_queryset(self, *args, **kwargs):

        return models.OtherSite.objects.filter(display = True)

class OtherSiteDetailView(DetailView):
    
    model = models.OtherSite
    context_object_name = "othersite"

    def get_context_data(self, *args, **kwargs):

        context = super(OtherSiteDetailView, self).get_context_data(*args, **kwargs)

        context["othersite_list"] = models.OtherSite.objects.filter(display = True)

        return context
