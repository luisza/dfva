from django.contrib import admin

# Register your models here.
from .models import (AuthenticateDataRequest,
                     AuthenticateRequest,
                     Institution,
                     NotificationURL)


class NotificationURLAdmin(admin.TabularInline):
    model = NotificationURL


class InstitutionAdmin(admin.ModelAdmin):
    inlines = [NotificationURLAdmin]

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(AuthenticateDataRequest)
admin.site.register(AuthenticateRequest)
