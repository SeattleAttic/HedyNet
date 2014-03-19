from django.contrib import admin

import profiles.models as models

admin.site.register(models.UserProfile)
admin.site.register(models.UserEmail)
admin.site.register(models.UserPhone)
admin.site.register(models.UserAddress)
admin.site.register(models.UserExternalSite)

class MemberStatusChangeAdmin(admin.ModelAdmin):
    list_display = ("profile", "changed_on", "new_status", "old_status")
    list_filter = ("changed_on", "new_status", "profile")
admin.site.register(models.MemberStatusChange, MemberStatusChangeAdmin)
