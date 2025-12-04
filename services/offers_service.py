from offers.models import Offer

def create_offer(buyer, listing, amount):
    """
    Create a new offer.
    """
    # Check if offer already exists? (Optional)
    
    offer = Offer.objects.create(
        buyer=buyer,
        listing=listing,
        amount=amount,
        status='pending'
    )
    return offer

def accept_offer(offer):
    """
    Accept an offer and reject others for the same listing?
    """
    offer.status = 'accepted'
    offer.save()
    # Logic to handle other offers or close listing could go here
    return offer
