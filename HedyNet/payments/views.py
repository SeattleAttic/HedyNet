from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.views.generic import TemplateView
from django.conf import settings

class SubscriptionTemplateView(TemplateView):
    template_name = "payments/subscriptions.html"

    def get_context_data(self, *args, **kwargs):

        context = super(SubscriptionTemplateView, self).get_context_data(
            *args, **kwargs)

        return context

class SubscriptionThanksTemplateView(TemplateView):
    template_name = "payments/subscription_thankyou.html"


class DonationTemplateView(TemplateView):
    template_name = "payments/donations.html"
    
    def get_context_data(self, *args, **kwargs):

        context = super(DonationTemplateView, self).get_context_data(*args, **kwargs)

        return context
        
class DonationThanksTemplateView(TemplateView):
    template_name = "payments/donation_thankyou.html"
