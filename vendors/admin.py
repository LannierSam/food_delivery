from django.contrib import admin
from .models import Vendor, MenuItem

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'distance', 'delivery_time', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['name', 'description']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'price', 'category', 'is_available']
    list_filter = ['category', 'is_available', 'vendor']
    search_fields = ['name', 'description']