from django.contrib import admin
from .models import Categories, Sessions, Threads, Posts, Doctors


# Register your models here.

@admin.register(Categories, Sessions, Threads, Posts, Doctors)
class BaseAdminRegister(admin.ModelAdmin):
    pass
