from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from listings.models import Listing

class ListingInline(admin.TabularInline):
    model = Listing
    extra = 0
    readonly_fields = ['title', 'category', 'price', 'status', 'created_at']
    can_delete = False
    show_change_link = True
    
    def has_add_permission(self, request, obj=None):
        return False

class UserAdmin(BaseUserAdmin):
    inlines = [ListingInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'get_listing_count']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    
    def get_listing_count(self, obj):
        return obj.listings.count()
    get_listing_count.short_description = 'Listings'

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
