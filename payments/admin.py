from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'offer', 'amount', 'status', 'transaction_id', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['buyer__username', 'offer__listing__title', 'transaction_id', 'upi_id']
    readonly_fields = ['created_at', 'completed_at', 'transaction_id']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('buyer', 'offer', 'offer__listing', 'offer__listing__seller')

