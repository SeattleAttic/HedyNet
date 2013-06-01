from django.contrib import admin

from .views import FAQSectionListView, FAQSectionDetailView, FAQItemDetailView

admin.site.register(FAQSectionListView)
admin.site.register(FAQSectionDetailView)
admin.site.register(FAQItemDetailView)
