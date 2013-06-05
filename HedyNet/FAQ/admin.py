from django.contrib import admin

from .views import FAQSection, FAQItem

class FAQSectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
admin.site.register(FAQSection, FAQSectionAdmin)

class FAQItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("question",)}
admin.site.register(FAQItem, FAQItemAdmin)
