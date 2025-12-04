from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='cart_entries')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'listing']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username}'s cart - {self.listing.title}"

