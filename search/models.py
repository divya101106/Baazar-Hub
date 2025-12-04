from django.db import models
from django.contrib.auth.models import User

class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    query = models.CharField(max_length=255)
    filters = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search '{self.query}' by {self.user.username}"
