from django.views.generic import DetailView, ListView

from profiles.views import AccessFieldPassDetailMixin, AccessFieldPassListView
from profiles.models import filter_access_levels, UserProfile
from profiles.access import access_levels

from .models import FAQSection, FAQItem

class FAQSectionListView(AccessFieldPassListView):
    
    model = FAQSection
    context_object_name = "faqsection_list"
    access_field_name = "access"

class FAQSectionDetailView(AccessFieldPassDetailMixin, DetailView):
    
    model = FAQSection
    context_object_name = "faqsection"
    access_field_name = "access"

    def get_context_data(self, *args, **kwargs):
        context = super(FAQSectionDetailView, self).get_context_data(**kwargs)

        # add the viewer's profile to this view
        self.viewer_profile = UserProfile.get_profile(self.request.user)

        valid_access_levels = access_levels(None, self.viewer_profile)
        context["faqsection_items"] = filter_access_levels(self.object.faqitem_set.all(), "access", valid_access_levels)

        return context

class FAQItemDetailView(AccessFieldPassDetailMixin, DetailView):
    
    model = FAQItem
    context_object_name = "faqitem"
    slug_url_kwarg = "faq_slug"
    section_url_kwarg = "section_slug"
    access_field_name = "access"
    
    def get_queryset(self):
        """Cut down the queryset based on the FAQ section's slug, so
        retrieval will work properly."""
        return FAQItem.objects.filter(
            section__slug = self.kwargs[self.section_url_kwarg]) 
