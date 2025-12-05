from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Dispute
from .forms import DisputeForm
from offers.models import Offer

@login_required
def create_dispute(request, offer_id=None):
    """Create a dispute for a transaction"""
    from payments.models import Payment
    
    # If offer_id is provided, pre-select it
    initial_data = {}
    if offer_id:
        offer = get_object_or_404(Offer, id=offer_id)
        # Verify user is involved in this transaction
        if request.user != offer.buyer and request.user != offer.listing.seller:
            messages.error(request, "You don't have permission to create a dispute for this transaction.")
            return redirect('user_profile')
        
        # Check if offer is accepted
        if offer.status != 'accepted':
            messages.error(request, "You can only create disputes for accepted transactions.")
            return redirect('user_profile')
        
        # Check if payment is completed
        try:
            payment = offer.payment
            if payment.status != 'completed':
                messages.error(request, "You can only create disputes for completed payments.")
                return redirect('user_profile')
        except:
            messages.error(request, "Payment not found. Please complete payment first.")
            return redirect('user_profile')
        
        # Check if dispute already exists
        existing_dispute = Dispute.objects.filter(transaction=offer, reporter=request.user).first()
        if existing_dispute:
            messages.info(request, "You have already submitted a dispute for this transaction.")
            return redirect('dispute_detail', dispute_id=existing_dispute.id)
        
        initial_data['transaction'] = offer
    else:
        # If no offer_id, check if user has any completed payments
        latest_payment = Payment.objects.filter(
            buyer=request.user,
            status='completed'
        ).select_related('offer', 'offer__listing').order_by('-completed_at').first()
        
        if latest_payment:
            # Pre-select the latest purchased item
            initial_data['transaction'] = latest_payment.offer
    
    if request.method == 'POST':
        form = DisputeForm(request.POST, user=request.user)
        if form.is_valid():
            dispute = form.save(commit=False)
            dispute.reporter = request.user
            
            # Verify user is involved in the transaction
            transaction = form.cleaned_data['transaction']
            if request.user != transaction.buyer and request.user != transaction.listing.seller:
                messages.error(request, "You don't have permission to create a dispute for this transaction.")
                return redirect('user_profile')
            
            # Check if payment is completed
            try:
                payment = transaction.payment
                if payment.status != 'completed':
                    messages.error(request, "You can only create disputes for completed payments.")
                    return redirect('user_profile')
            except:
                messages.error(request, "Payment not found. Please complete payment first.")
                return redirect('user_profile')
            
            # Verify this is the latest purchased item (only for buyers)
            if request.user == transaction.buyer:
                latest_payment = Payment.objects.filter(
                    buyer=request.user,
                    status='completed'
                ).order_by('-completed_at').first()
                
                if latest_payment and latest_payment.offer.id != transaction.id:
                    messages.error(request, "You can only create a dispute for your latest purchased item.")
                    return redirect('user_profile')
            
            dispute.save()
            
            # Create notification for the other party (buyer or seller)
            from notifications.utils import create_notification
            other_user = transaction.buyer if request.user == transaction.listing.seller else transaction.listing.seller
            create_notification(
                user=other_user,
                notification_type='message_received',  # Reusing type
                title='Dispute Reported',
                message=f"{request.user.username} has reported a dispute for transaction '{transaction.listing.title}'",
                related_user=request.user,
                related_offer=transaction,
                related_listing=transaction.listing
            )
            
            messages.success(request, "Dispute submitted successfully. An admin will review it shortly.")
            return redirect('dispute_detail', dispute_id=dispute.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DisputeForm(user=request.user, initial=initial_data)
        
        # Check if user has any completed payments
        from payments.models import Payment
        latest_payment = Payment.objects.filter(
            buyer=request.user,
            status='completed'
        ).select_related('offer', 'offer__listing').order_by('-completed_at').first()
        
        if not latest_payment:
            messages.warning(request, "You don't have any completed purchases yet. You can only create disputes for items you have purchased.")
            return redirect('user_profile')
    
    return render(request, 'disputes/create_dispute.html', {'form': form})

@login_required
def dispute_detail(request, dispute_id):
    """View dispute details"""
    dispute = get_object_or_404(Dispute, id=dispute_id)
    
    # Only reporter or admin can view
    if request.user != dispute.reporter and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this dispute.")
        return redirect('user_profile')
    
    return render(request, 'disputes/dispute_detail.html', {'dispute': dispute})

@login_required
def my_disputes(request):
    """View user's disputes"""
    disputes = Dispute.objects.filter(reporter=request.user).select_related('transaction', 'transaction__listing', 'transaction__buyer', 'transaction__listing__seller').order_by('-created_at')
    
    return render(request, 'disputes/my_disputes.html', {'disputes': disputes})
