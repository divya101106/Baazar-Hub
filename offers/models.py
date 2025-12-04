from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing

class Offer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers_made')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='offers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer of {self.amount} for {self.listing.title} by {self.buyer.username}"
