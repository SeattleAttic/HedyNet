from django.views.generic import DetailView
from .models import FAQSection, FAQItem

class FAQSectionListView():
    
    model = FAQSection
    context_object_name = "faqsection_list"

class FAQSectionDetailView(DetailView):
    
    model = FAQSection
    context_object_name = "faqsection"

class FAQItemDetailView(DetailView):
    
    model = FAQItem
    context_object_name = "faqitem"
    slug_url_kwarg = "faq_slug"
    section_url_kwarg = "section_slug"
    
    get_queryset():
        """Cut down the queryset based on the FAQ section's slug, so
        retrieval will work properly."""
        return FAQSection.objects.all() # TODO: use the faq section slug to filter
