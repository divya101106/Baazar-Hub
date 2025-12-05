from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import uuid
from .models import Payment
from .forms import PaymentForm
from offers.models import Offer
from notifications.utils import create_notification

# Fixed UPI credentials for dummy payment
DUMMY_UPI_ID = 'pay@paytm'
DUMMY_UPI_PIN = '1234'

@login_required
def payment_page(request, offer_id):
    """Payment page for an accepted offer"""
    offer = get_object_or_404(Offer, id=offer_id)
    
    # Verify user is the buyer
    if request.user != offer.buyer:
        messages.error(request, "You don't have permission to pay for this offer.")
        return redirect('user_profile')
    
    # Check if offer is accepted
    if offer.status != 'accepted':
        messages.error(request, "You can only pay for accepted offers.")
        return redirect('user_profile')
    
    # Check if payment already exists
    payment, created = Payment.objects.get_or_create(
        offer=offer,
        defaults={
            'buyer': request.user,
            'amount': offer.amount,
            'status': 'pending'
        }
    )
    
    # If payment is already completed
    if payment.status == 'completed':
        messages.info(request, "Payment for this offer has already been completed.")
        return redirect('payment_success', offer_id=offer_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            upi_id = form.cleaned_data['upi_id']
            upi_pin = form.cleaned_data['upi_pin']
            
            # Verify UPI credentials (dummy check)
            if upi_id == DUMMY_UPI_ID and upi_pin == DUMMY_UPI_PIN:
                # Payment successful
                payment.status = 'completed'
                payment.upi_id = upi_id
                payment.transaction_id = f"TXN{str(uuid.uuid4())[:8].upper()}"
                payment.completed_at = timezone.now()
                payment.save()
                
                # Create notification for seller
                create_notification(
                    user=offer.listing.seller,
                    notification_type='offer_accepted',  # Reusing type
                    title='Payment Received!',
                    message=f"Payment of ₹{offer.amount} has been received for '{offer.listing.title}' from {request.user.username}.",
                    related_user=request.user,
                    related_offer=offer,
                    related_listing=offer.listing
                )
                
                messages.success(request, "Payment completed successfully! The item is now booked.")
                return redirect('payment_success', offer_id=offer_id)
            else:
                messages.error(request, "Invalid UPI ID or PIN. Please use: UPI ID: pay@paytm, PIN: 1234")
    else:
        form = PaymentForm()
    
    context = {
        'offer': offer,
        'form': form,
        'payment': payment,
        'dummy_upi_id': DUMMY_UPI_ID,
    }
    
    return render(request, 'payments/payment_page.html', context)

@login_required
def payment_success(request, offer_id):
    """Payment success page"""
    offer = get_object_or_404(Offer, id=offer_id)
    
    # Verify user is the buyer
    if request.user != offer.buyer:
        messages.error(request, "You don't have permission to view this payment.")
        return redirect('user_profile')
    
    try:
        payment = Payment.objects.get(offer=offer)
    except Payment.DoesNotExist:
        messages.error(request, "Payment not found.")
        return redirect('user_profile')
    
    context = {
        'offer': offer,
        'payment': payment,
    }
    
    return render(request, 'payments/payment_success.html', context)

