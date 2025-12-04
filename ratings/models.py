from django.db import models
from django.contrib.auth.models import User
from offers.models import Offer

class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    transaction = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.score} for {self.rated_user.username} by {self.rater.username}"
