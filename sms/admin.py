from django.contrib import admin

# Register your models here.
from .models import Customer, MainSetup

admin.site.register(Customer)
admin.site.register(MainSetup)

