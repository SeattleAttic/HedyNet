from django.views.generic import DetailView, ListView
from .models import FAQSection, FAQItem

class FAQSectionListView(ListView):
    
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
    
    def get_queryset(self):
        """Cut down the queryset based on the FAQ section's slug, so
        retrieval will work properly."""
        return FAQItem.objects.filter(
            section__slug = self.kwargs[self.section_url_kwarg]) 
