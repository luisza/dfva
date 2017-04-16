from django.contrib import admin

# Register your models here.
from .models import (Authenticate_Data_Request,
                     Authenticate_Request,
                     Institution,
                     Notification_URL)


class Notification_URLAdmin(admin.TabularInline):
    model = Notification_URL


class InstitutionAdmin(admin.ModelAdmin):
    inlines = [Notification_URLAdmin]

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Authenticate_Data_Request)
admin.site.register(Authenticate_Request)