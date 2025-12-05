from django.urls import path
from .views import get_notifications, mark_notification_read, mark_all_read, unread_notifications_count

urlpatterns = [
    path('api/notifications/', get_notifications, name='get_notifications'),
    path('api/notifications/<int:notification_id>/read/', mark_notification_read, name='mark_notification_read'),
    path('api/notifications/mark-all-read/', mark_all_read, name='mark_all_notifications_read'),
    path('api/notifications/count/', unread_notifications_count, name='unread_notifications_count'),
]

