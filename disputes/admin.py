from django.contrib import admin
from .models import Dispute

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'transaction', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['reporter__username', 'transaction__listing__title', 'reason']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Dispute Information', {
            'fields': ('reporter', 'transaction', 'status', 'created_at')
        }),
        ('Details', {
            'fields': ('reason',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('reporter', 'transaction', 'transaction__listing', 'transaction__buyer', 'transaction__listing__seller')
    
    actions = ['mark_resolved', 'mark_closed']
    
    def mark_resolved(self, request, queryset):
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} dispute(s) marked as resolved.', admin.SUCCESS)
    mark_resolved.short_description = "Mark selected disputes as resolved"
    
    def mark_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} dispute(s) marked as closed.', admin.SUCCESS)
    mark_closed.short_description = "Mark selected disputes as closed"
