from django.contrib import admin
from .models import OrganizationlDetials
# Register your models here.

@admin.register(OrganizationlDetials)
class orgDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'gstin')
