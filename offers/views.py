from rest_framework import viewsets, permissions
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Offer
from .serializers import OfferSerializer
from listings.models import Listing

class OfferViewSet(viewsets.ModelViewSet):
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Users can ONLY see offers they made OR offers on their listings (privacy restriction)
        return Offer.objects.filter(Q(buyer=user) | Q(listing__seller=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

@login_required
def create_offer(request):
    """Create an offer from HTML form"""
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        amount = request.POST.get('amount')
        
        try:
            listing = get_object_or_404(Listing, id=listing_id, status='approved')
            
            # Don't allow creating offers on own listings
            if listing.seller == request.user:
                messages.error(request, "You cannot make an offer on your own listing.")
                return redirect('listing_detail', pk=listing_id)
            
            amount = float(amount)
            if amount <= 0:
                messages.error(request, "Offer amount must be greater than zero.")
                return redirect('listing_detail', pk=listing_id)
            
            # Create or get existing offer
            offer, created = Offer.objects.get_or_create(
                buyer=request.user,
                listing=listing,
                defaults={'amount': amount, 'status': 'pending'}
            )
            
            if created:
                messages.success(request, f"Offer of ₹{amount} submitted! You can now chat with the seller.")
                # Create notification for seller
                from notifications.utils import create_notification
                create_notification(
                    user=listing.seller,
                    notification_type='offer_received',
                    title='New Offer Received',
                    message=f"{request.user.username} made an offer of ₹{amount} on your listing '{listing.title}'",
                    related_user=request.user,
                    related_offer=offer,
                    related_listing=listing
                )
            else:
                offer.amount = amount
                offer.status = 'pending'
                offer.save()
                messages.info(request, f"Offer updated to ₹{amount}.")
            
            # Redirect to chat
            return redirect('chat_with_user', user_id=listing.seller.id, offer_id=offer.id)
            
        except (ValueError, TypeError):
            messages.error(request, "Invalid offer amount.")
            return redirect('listing_detail', pk=listing_id)
        except Exception as e:
            messages.error(request, f"Error creating offer: {str(e)}")
            return redirect('listing_detail', pk=listing_id)
    
    return redirect('home')

@login_required
def accept_offer(request, offer_id):
    """Accept an offer"""
    offer = get_object_or_404(Offer, id=offer_id)
    
    # Only the seller can accept offers on their listings
    if request.user != offer.listing.seller:
        messages.error(request, "You don't have permission to accept this offer.")
        return redirect('user_profile')
    
    # Only pending offers can be accepted
    if offer.status != 'pending':
        messages.error(request, f"This offer has already been {offer.status}.")
        return redirect('user_profile')
    
    # Accept the offer
    offer.status = 'accepted'
    offer.save()
    
    # Create notification for buyer
    from notifications.utils import create_notification
    create_notification(
        user=offer.buyer,
        notification_type='offer_accepted',
        title='Offer Accepted!',
        message=f"Your offer of ₹{offer.amount} for '{offer.listing.title}' has been accepted by the seller.",
        related_user=request.user,
        related_offer=offer,
        related_listing=offer.listing
    )
    
    messages.success(request, f"Offer of ₹{offer.amount} has been accepted!")
    return redirect('user_profile')

@login_required
def reject_offer(request, offer_id):
    """Reject an offer"""
    offer = get_object_or_404(Offer, id=offer_id)
    
    # Only the seller can reject offers on their listings
    if request.user != offer.listing.seller:
        messages.error(request, "You don't have permission to reject this offer.")
        return redirect('user_profile')
    
    # Only pending offers can be rejected
    if offer.status != 'pending':
        messages.error(request, f"This offer has already been {offer.status}.")
        return redirect('user_profile')
    
    # Reject the offer
    offer.status = 'rejected'
    offer.save()
    
    # Create notification for buyer
    from notifications.utils import create_notification
    create_notification(
        user=offer.buyer,
        notification_type='offer_rejected',
        title='Offer Rejected',
        message=f"Your offer of ₹{offer.amount} for '{offer.listing.title}' has been rejected by the seller.",
        related_user=request.user,
        related_offer=offer,
        related_listing=offer.listing
    )
    
    messages.info(request, f"Offer of ₹{offer.amount} has been rejected.")
    return redirect('user_profile')
