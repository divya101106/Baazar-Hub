"""
Utility functions for creating notifications
"""
from .models import Notification

def create_notification(user, notification_type, title, message, related_user=None, related_offer=None, related_listing=None):
    """Create a notification for a user"""
    notification = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        related_user=related_user,
        related_offer=related_offer,
        related_listing=related_listing
    )
    return notification

