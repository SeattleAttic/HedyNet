from django.contrib import admin

from .views import FAQSection, FAQItem

admin.site.register(FAQSection)
admin.site.register(FAQItem)
