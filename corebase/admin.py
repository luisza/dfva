from django.contrib import admin
from .models import NotificationURL, Institution

# Register your models here.


class NotificationURLAdmin(admin.TabularInline):
    model = NotificationURL


class InstitutionAdmin(admin.ModelAdmin):
    inlines = [NotificationURLAdmin]


admin.site.register(Institution, InstitutionAdmin)
