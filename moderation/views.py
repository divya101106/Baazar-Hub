from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import ModerationQueue
from .serializers import ModerationQueueSerializer

@staff_member_required
def moderation_dashboard(request):
    queue = ModerationQueue.objects.filter(status='pending').order_by('created_at')
    return render(request, 'moderation/dashboard.html', {'queue': queue})

@staff_member_required
def moderate_action(request, pk, action):
    entry = get_object_or_404(ModerationQueue, pk=pk)
    if action == 'approve':
        entry.status = 'reviewed'
        entry.reviewed_at = timezone.now()
        entry.save()
        entry.listing.status = 'approved'
        entry.listing.save()
        # Trigger saved search alerts (signal will handle this)
    elif action == 'reject':
        entry.status = 'reviewed'
        entry.reviewed_at = timezone.now()
        entry.save()
        entry.listing.status = 'rejected'
        entry.listing.save()
    return redirect('moderation_dashboard')

class ModerationQueueViewSet(viewsets.ModelViewSet):
    queryset = ModerationQueue.objects.filter(status='pending')
    serializer_class = ModerationQueueSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        entry = self.get_object()
        entry.status = 'reviewed'
        entry.reviewed_at = timezone.now()
        entry.save()
        
        # Update listing status
        listing = entry.listing
        listing.status = 'approved'
        listing.save()
        
        # Trigger saved search alerts (signal will handle this)
        
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        entry = self.get_object()
        entry.status = 'reviewed'
        entry.reviewed_at = timezone.now()
        entry.save()
        
        # Update listing status
        listing = entry.listing
        listing.status = 'rejected'
        listing.save()
        
        return Response({'status': 'rejected'})
