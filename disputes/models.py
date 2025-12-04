from django.db import models
from django.contrib.auth.models import User
from offers.models import Offer

class Dispute(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disputes_reported')
    transaction = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='disputes')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute on {self.transaction} by {self.reporter.username}"
