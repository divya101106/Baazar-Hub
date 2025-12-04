from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'listing__title']
    readonly_fields = ['added_at']

