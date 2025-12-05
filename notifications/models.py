from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notification(models.Model):
    """Notification model for user notifications"""
    NOTIFICATION_TYPES = [
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('offer_rejected', 'Offer Rejected'),
        ('message_received', 'Message Received'),
        ('chat_started', 'Chat Started'),
        ('saved_search_match', 'Saved Search Match'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    related_offer = models.ForeignKey('offers.Offer', on_delete=models.CASCADE, null=True, blank=True)
    related_listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def get_absolute_url(self):
        """Get URL related to this notification"""
        if self.notification_type == 'offer_received' and self.related_offer:
            from django.urls import reverse
            return reverse('chat_with_user', args=[self.related_user.id, self.related_offer.id]) if self.related_user and self.related_offer else '#'
        elif self.notification_type == 'message_received' and self.related_user:
            from django.urls import reverse
            return reverse('chat_with_user', args=[self.related_user.id])
        elif self.notification_type == 'saved_search_match' and self.related_listing:
            from django.urls import reverse
            return reverse('listing_detail', args=[self.related_listing.id])
        elif self.related_listing:
            from django.urls import reverse
            return reverse('listing_detail', args=[self.related_listing.id])
        return '#'
    
    @property
    def time_ago(self):
        """Return human-readable time ago"""
        delta = timezone.now() - self.created_at
        if delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
