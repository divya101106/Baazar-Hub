from rest_framework import viewsets, permissions
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializer
from offers.models import Offer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Users can only see messages where they are sender or receiver
        return Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

@login_required
def chat_with_user(request, user_id, offer_id=None):
    """Chat view between two users"""
    other_user = get_object_or_404(User, id=user_id)
    
    # Users can only chat if they have a transaction (offer) together
    if offer_id:
        offer = get_object_or_404(Offer, id=offer_id)
        # Verify user is involved in this offer
        if request.user != offer.buyer and request.user != offer.listing.seller:
            messages.error(request, "You don't have permission to view this chat.")
            return redirect('home')
    else:
        # Check if users have any offers together
        has_offer = Offer.objects.filter(
            Q(buyer=request.user, listing__seller=other_user) |
            Q(buyer=other_user, listing__seller=request.user)
        ).exists()
        
        if not has_offer:
            messages.error(request, "You can only chat with users you have a transaction with.")
            return redirect('home')
        offer = None
    
    # Get messages between these users related to this offer
    # Users can only see messages they sent or received (privacy restriction)
    if offer:
        chat_messages = Message.objects.filter(
            offer=offer
        ).filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).select_related('sender', 'receiver').order_by('timestamp')
    else:
        chat_messages = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)
        ).select_related('sender', 'receiver').order_by('timestamp')
    
    # Mark messages as read
    chat_messages.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                offer=offer,
                content=content
            )
            messages.success(request, "Message sent!")
            
            # Create notification for receiver
            from notifications.utils import create_notification
            notification_title = f"New message from {request.user.username}"
            notification_message = content[:100] + "..." if len(content) > 100 else content
            create_notification(
                user=other_user,
                notification_type='message_received',
                title=notification_title,
                message=notification_message,
                related_user=request.user,
                related_offer=offer,
                related_listing=offer.listing if offer else None
            )
            
            return redirect('chat_with_user', user_id=user_id, offer_id=offer_id if offer else None)
        else:
            messages.error(request, "Message cannot be empty.")
    
    return render(request, 'chat/chat.html', {
        'other_user': other_user,
        'chat_messages': chat_messages,
        'offer': offer
    })
