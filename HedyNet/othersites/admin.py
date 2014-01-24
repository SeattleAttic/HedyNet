from django.contrib import admin

from othersites import models

class OtherSiteAdmin(admin.ModelAdmin):
    list_display = ("name", 'display', "order", "link")
    list_filter = ("display",)
    list_editable = ("order",)
admin.site.register(models.OtherSite, OtherSiteAdmin)
