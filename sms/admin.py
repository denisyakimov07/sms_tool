from django.contrib import admin

# Register your models here.
from .models import Customer, MainSetup


class MainSetupAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Customer)
admin.site.register(MainSetup,MainSetupAdmin)

