"""
Signals for saved search alerts
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from listings.models import Listing
from .models import SavedSearch
from notifications.utils import create_notification
from django.db.models import Q

# Store previous status to detect changes
_previous_status = {}

@receiver(pre_save, sender=Listing)
def store_previous_status(sender, instance, **kwargs):
    """Store the previous status before save"""
    if instance.pk:
        try:
            previous = Listing.objects.get(pk=instance.pk)
            _previous_status[instance.pk] = previous.status
        except Listing.DoesNotExist:
            _previous_status[instance.pk] = None
    else:
        _previous_status[instance.pk] = None

@receiver(post_save, sender=Listing)
def check_saved_searches_on_approval(sender, instance, created, **kwargs):
    """
    When a listing is approved, check all saved searches and create alerts for matches.
    """
    previous_status = _previous_status.get(instance.pk, None)
    
    # Only trigger when listing status changes to 'approved' (not just when it's approved)
    if instance.status == 'approved' and previous_status != 'approved':
        # Get all saved searches
        saved_searches = SavedSearch.objects.all()
        
        for saved_search in saved_searches:
            # Skip if this is the user's own listing
            if instance.seller == saved_search.user:
                continue
            
            # Check if listing matches saved search
            if matches_saved_search(instance, saved_search):
                # Create notification for the user
                create_notification(
                    user=saved_search.user,
                    notification_type='saved_search_match',
                    title='New Listing Matches Your Saved Search',
                    message=f"A new listing '{instance.title}' matches your saved search '{saved_search.query}'",
                    related_listing=instance
                )
    
    # Clean up
    if instance.pk in _previous_status:
        del _previous_status[instance.pk]

def matches_saved_search(listing, saved_search):
    """
    Check if a listing matches a saved search criteria.
    """
    query = saved_search.query.lower().strip()
    filters = saved_search.filters or {}
    
    # Check keyword match
    if query:
        listing_text = (listing.title + " " + listing.description).lower()
        # Check if any word from query is in listing
        query_words = query.split()
        if not any(word in listing_text for word in query_words if len(word) > 2):
            return False
    
    # Check category filter
    if filters.get('category_id'):
        if listing.category_id != filters.get('category_id'):
            return False
    
    # Check price range filter
    min_price = filters.get('min_price')
    max_price = filters.get('max_price')
    
    if min_price is not None and listing.price < float(min_price):
        return False
    
    if max_price is not None and listing.price > float(max_price):
        return False
    
    return True

