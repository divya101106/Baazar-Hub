from django.contrib import admin
from .models import ModerationQueue

@admin.register(ModerationQueue)
class ModerationQueueAdmin(admin.ModelAdmin):
    list_display = ['listing', 'status', 'reason', 'created_at', 'reviewed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['listing__title', 'listing__seller__username', 'reason']
    readonly_fields = ['created_at', 'reviewed_at']
    fieldsets = (
        ('Listing Information', {
            'fields': ('listing',)
        }),
        ('Moderation Details', {
            'fields': ('status', 'reason', 'created_at', 'reviewed_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('listing', 'listing__seller', 'listing__category')
