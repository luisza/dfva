from django.contrib import admin

# Register your models here.
from .models import (AuthenticateDataRequest,
                     AuthenticateRequest)


admin.site.register(AuthenticateDataRequest)
admin.site.register(AuthenticateRequest)
