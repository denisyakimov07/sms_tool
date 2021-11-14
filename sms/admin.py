from django.contrib import admin

# Register your models here.
from .models import Customer, Main_setup

admin.site.register(Customer)
admin.site.register(Main_setup)
