from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'offer', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['sender__username', 'receiver__username', 'content']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('sender', 'receiver', 'offer')
