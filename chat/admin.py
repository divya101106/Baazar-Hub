from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content_preview', 'offer', 'timestamp', 'is_read', 'delete_action']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['sender__username', 'receiver__username', 'content']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('sender', 'receiver', 'offer', 'offer__listing')
    
    def content_preview(self, obj):
        """Show preview of message content"""
        preview = obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
        return format_html('<span title="{}">{}</span>', obj.content, preview)
    content_preview.short_description = 'Content'
    
    def delete_action(self, obj):
        """Add delete button for each message"""
        delete_url = reverse('admin:chat_message_delete', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="background-color: #dc3545; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none; font-size: 12px;">Delete</a>',
            delete_url
        )
    delete_action.short_description = 'Delete'
    delete_action.allow_tags = True
    
    def has_delete_permission(self, request, obj=None):
        """Only admins can delete messages"""
        return request.user.is_staff
    
    def delete_model(self, request, obj):
        """Override delete to add logging"""
        sender = obj.sender.username
        receiver = obj.receiver.username
        obj.delete()
        self.message_user(request, f'Message from {sender} to {receiver} has been deleted.', level='success')
