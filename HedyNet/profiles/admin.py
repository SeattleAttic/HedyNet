from django.contrib import admin

import profiles.models as models

admin.site.register(models.UserProfile)
admin.site.register(models.UserEmail)
admin.site.register(models.UserPhone)
admin.site.register(models.UserAddress)
