"""
Signals for saved search alerts
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from listings.models import Listing
from .models import SavedSearch
from notifications.utils import create_notification
from django.db.models import Q
import threading

# Thread-local storage for previous status (thread-safe)
_thread_local = threading.local()

def get_previous_status(instance_pk):
    """Get previous status from thread-local storage"""
    if not hasattr(_thread_local, 'previous_status'):
        _thread_local.previous_status = {}
    return _thread_local.previous_status.get(instance_pk, None)

def set_previous_status(instance_pk, status):
    """Set previous status in thread-local storage"""
    if not hasattr(_thread_local, 'previous_status'):
        _thread_local.previous_status = {}
    _thread_local.previous_status[instance_pk] = status

def clear_previous_status(instance_pk):
    """Clear previous status from thread-local storage"""
    if hasattr(_thread_local, 'previous_status'):
        _thread_local.previous_status.pop(instance_pk, None)

@receiver(pre_save, sender=Listing)
def store_previous_status(sender, instance, **kwargs):
    """Store the previous status before save"""
    if instance.pk:
        try:
            previous = Listing.objects.get(pk=instance.pk)
            set_previous_status(instance.pk, previous.status)
        except Listing.DoesNotExist:
            set_previous_status(instance.pk, None)
    else:
        # New listing, no previous status
        set_previous_status(instance.pk, None)

@receiver(post_save, sender=Listing)
def check_saved_searches_on_approval(sender, instance, created, **kwargs):
    """
    When a listing is approved, check all saved searches and create alerts for matches.
    """
    try:
        previous_status = get_previous_status(instance.pk)
        
        # Only trigger when listing status changes to 'approved' (not just when it's approved)
        if instance.status == 'approved' and previous_status != 'approved':
            # Get all saved searches
            saved_searches = SavedSearch.objects.all()
            
            for saved_search in saved_searches:
                # Skip if this is the user's own listing
                if instance.seller == saved_search.user:
                    continue
                
                # Check if listing matches saved search
                try:
                    if matches_saved_search(instance, saved_search):
                        # Create notification for the user
                        create_notification(
                            user=saved_search.user,
                            notification_type='saved_search_match',
                            title='New Listing Matches Your Saved Search',
                            message=f"A new listing '{instance.title}' matches your saved search '{saved_search.query}'",
                            related_listing=instance
                        )
                except Exception as e:
                    # Log error but don't prevent listing approval
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Error checking saved search match: {e}")
    finally:
        # Always clean up, even if there's an error
        if instance.pk:
            clear_previous_status(instance.pk)

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
        try:
            category_id = int(filters.get('category_id'))
            if listing.category_id != category_id:
                return False
        except (ValueError, TypeError):
            # Invalid category_id, skip this filter
            pass
    
    # Check price range filter with error handling
    min_price = filters.get('min_price')
    max_price = filters.get('max_price')
    
    if min_price is not None:
        try:
            min_price_float = float(min_price)
            if listing.price < min_price_float:
                return False
        except (ValueError, TypeError):
            # Invalid min_price, skip this filter
            pass
    
    if max_price is not None:
        try:
            max_price_float = float(max_price)
            if listing.price > max_price_float:
                return False
        except (ValueError, TypeError):
            # Invalid max_price, skip this filter
            pass
    
    return True

