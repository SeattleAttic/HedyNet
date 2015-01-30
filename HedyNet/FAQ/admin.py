from django.contrib import admin

from .models import FAQSection, FAQItem

class FAQSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "access")
    prepopulated_fields = {"slug": ("title",)}
admin.site.register(FAQSection, FAQSectionAdmin)

class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("topic", "section", "access")
    prepopulated_fields = {"slug": ("topic",)}
    list_filter = ("section",)
admin.site.register(FAQItem, FAQItemAdmin)
