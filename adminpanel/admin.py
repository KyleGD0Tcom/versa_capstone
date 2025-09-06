from django.contrib import admin
from .models import UserProfile, UserSettings, InventoryItem

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'role', 'status', 'employee_type', 'date_of_joining']
    list_filter = ['department', 'status', 'employee_type']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'department']
    readonly_fields = ['date_of_joining']

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'timezone', 'date_format', 'updated_at']
    list_filter = ['timezone', 'date_format']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['item_code', 'unit_item', 'category', 'department', 'quantity', 'unit_price', 'date_received']
    list_filter = ['category', 'department', 'date_received']
    search_fields = ['item_code', 'unit_item', 'details', 'supplier']
    readonly_fields = ['item_code']
