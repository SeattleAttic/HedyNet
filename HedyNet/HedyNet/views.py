from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.conf import settings

import othersites

class HomeTemplateView(TemplateView):
    template_name = "home_indiegogo.html"

    def get_context_data(self, *args, **kwargs):

        context = super(HomeTemplateView, self).get_context_data(
            *args, **kwargs)

        try:
            context["twitter"] = othersites.models.OtherSite.objects.get(slug="twitter")
        except:
            pass

        return context

