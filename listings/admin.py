from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from .models import Listing, ListingImage, Category
from moderation.models import ModerationQueue

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'price', 'status', 'created_at', 'flags']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'seller__username']
    readonly_fields = ['created_at', 'updated_at', 'flags', 'seller']
    list_editable = ['status']  # Allow quick status change
    actions = ['approve_listings', 'reject_listings']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'seller', 'category', 'price')
        }),
        ('Status & Moderation', {
            'fields': ('status', 'flags', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('seller', 'category').prefetch_related('images')
    
    def approve_listings(self, request, queryset):
        """Admin action to approve selected listings"""
        # Update each listing individually to trigger signals
        for listing in queryset:
            listing.status = 'approved'
            listing.save()
            # Update moderation queue
            ModerationQueue.objects.filter(listing=listing, status='pending').update(
                status='reviewed',
                reviewed_at=timezone.now(),
                reason='Approved by admin'
            )
        updated = queryset.count()
        self.message_user(request, f'{updated} listing(s) approved successfully.', messages.SUCCESS)
    approve_listings.short_description = "Approve selected listings"
    
    def reject_listings(self, request, queryset):
        """Admin action to reject selected listings"""
        from notifications.utils import create_notification
        # Update each listing individually to trigger signals (ensures cleanup in signals)
        for listing in queryset:
            listing.status = 'rejected'
            listing.save()  # This triggers pre_save and post_save signals (ensures cleanup)
            # Update moderation queue
            ModerationQueue.objects.filter(listing=listing, status='pending').update(
                status='reviewed',
                reason='Rejected by admin'
            )
            # Create notification for seller
            create_notification(
                user=listing.seller,
                notification_type='offer_rejected',  # Reusing type
                title='Listing Rejected',
                message=f"Your listing '{listing.title}' has been rejected. Please review the guidelines and create a new listing.",
                related_listing=listing
            )
        updated = queryset.count()
        self.message_user(request, f'{updated} listing(s) rejected.', messages.WARNING)
    reject_listings.short_description = "Reject selected listings"

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'image', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['listing__title']
    readonly_fields = ['uploaded_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('listing')
