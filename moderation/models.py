from django.db import models
from listings.models import Listing

class ModerationQueue(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='moderation_entries')
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Moderation for {self.listing.title}"
