from django.db import models
from django.contrib.auth.models import User
from offers.models import Offer

class Payment(models.Model):
    """Payment model for tracking transactions"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, related_name='payment')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    upi_id = models.CharField(max_length=100, blank=True)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment of ₹{self.amount} for {self.offer.listing.title} - {self.status}"

