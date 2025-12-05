from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Notification

@login_required
@require_http_methods(["GET"])
def get_notifications(request):
    """API endpoint to fetch user notifications"""
    # Get both read and unread notifications (latest 10)
    notifications = Notification.objects.filter(user=request.user).select_related('related_user', 'related_offer', 'related_listing').order_by('-created_at')[:10]
    
    notifications_data = []
    for notification in notifications:
            notifications_data.append({
                'id': notification.id,
                'type': notification.notification_type,
                'title': notification.title,
                'message': notification.message,
                'time_ago': notification.time_ago,
                'is_read': notification.is_read,
                'related_user': notification.related_user.username if notification.related_user else None,
                'url': notification.get_absolute_url(),
            })
    
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': unread_count
    })

@login_required
@require_http_methods(["POST"])
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)

@login_required
@require_http_methods(["POST"])
def mark_all_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})

@login_required
@require_http_methods(["GET"])
def unread_notifications_count(request):
    """Get count of unread notifications"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})
