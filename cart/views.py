from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Cart
from listings.models import Listing

@login_required
def cart_view(request):
    """View user's cart"""
    cart_items = Cart.objects.filter(user=request.user).select_related('listing', 'listing__seller', 'listing__category').prefetch_related('listing__images')
    total = sum(item.listing.price for item in cart_items)
    
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, listing_id):
    """Add listing to cart"""
    listing = get_object_or_404(Listing, id=listing_id, status='approved')
    
    # Don't allow adding own listings
    if listing.seller == request.user:
        messages.error(request, "You cannot add your own listing to cart.")
        return redirect('listing_detail', pk=listing_id)
    
    # Check if already in cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        listing=listing
    )
    
    if created:
        messages.success(request, f"{listing.title} added to cart!")
    else:
        messages.info(request, f"{listing.title} is already in your cart.")
    
    return redirect('listing_detail', pk=listing_id)

@login_required
def remove_from_cart(request, cart_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    listing_title = cart_item.listing.title
    cart_item.delete()
    messages.success(request, f"{listing_title} removed from cart.")
    return redirect('cart_view')

@login_required
def buy_now(request, listing_id):
    """Buy now - create offer, auto-accept, and redirect to payment"""
    listing = get_object_or_404(Listing, id=listing_id, status='approved')
    
    # Don't allow buying own listings
    if listing.seller == request.user:
        messages.error(request, "You cannot buy your own listing.")
        return redirect('listing_detail', pk=listing_id)
    
    from offers.models import Offer
    from payments.models import Payment
    
    # Create or get offer with listing price and auto-accept it
    offer, created = Offer.objects.get_or_create(
        buyer=request.user,
        listing=listing,
        defaults={'amount': listing.price, 'status': 'accepted'}
    )
    
    # If offer already exists but not accepted, accept it
    if not created and offer.status != 'accepted':
        offer.status = 'accepted'
        offer.save()
    
    # Check if payment already exists
    try:
        payment = Payment.objects.get(offer=offer)
        if payment.status == 'completed':
            messages.info(request, "Payment for this item has already been completed.")
            return redirect('payment_success', offer_id=offer.id)
        else:
            # Payment exists but not completed, redirect to payment page
            return redirect('payment_page', offer_id=offer.id)
    except Payment.DoesNotExist:
        # No payment exists, create one and redirect to payment page
        Payment.objects.create(
            offer=offer,
            buyer=request.user,
            amount=offer.amount,
            status='pending'
        )
        
        # Create notification for seller
        from notifications.utils import create_notification
        create_notification(
            user=listing.seller,
            notification_type='offer_accepted',
            title='Buy Now - Payment Pending',
            message=f"{request.user.username} wants to buy '{listing.title}' for ₹{listing.price}. Waiting for payment.",
            related_user=request.user,
            related_offer=offer,
            related_listing=listing
        )
        
        messages.success(request, f"Proceed to payment for {listing.title}")
        return redirect('payment_page', offer_id=offer.id)

