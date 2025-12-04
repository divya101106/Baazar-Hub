from listings.models import Listing, ListingImage
from services.moderation_service import check_spam_score, should_moderate, validate_image
from moderation.models import ModerationQueue
from utils.image_validation import validate_images
from django.core.exceptions import ValidationError

def create_listing(user, data, images=None):
    """
    Create a new listing, run moderation checks, and save.
    Validates images and applies moderation rules.
    """
    title = data.get('title')
    description = data.get('description')
    
    # Validate required fields
    if not title or len(title.strip()) < 10:
        raise ValidationError("Title must be at least 10 characters long")
    
    if not description or len(description.strip()) < 50:
        raise ValidationError("Description must be at least 50 characters long")
    
    price = data.get('price')
    if not price or price <= 0:
        raise ValidationError("Price must be greater than zero")
    
    # Validate images if provided
    valid_images = []
    if images:
        is_valid, error_msg, valid_images = validate_images(images)
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Additional image safety check
        for image in valid_images:
            if not validate_image(image):
                raise ValidationError(f"Image {image.name} failed safety validation")
    
    # Calculate spam score
    spam_score = check_spam_score(title, description)
    
    # ALL listings start as pending - admin must approve
    status = 'pending'
    
    # Create listing
    listing = Listing.objects.create(
        seller=user,
        title=title.strip(),
        description=description.strip(),
        price=price,
        category_id=data.get('category_id'),
        status=status,
        flags=spam_score
    )
    
    # Create listing images
    if valid_images:
        for image in valid_images:
            ListingImage.objects.create(listing=listing, image=image)
    
    # Always add to moderation queue for admin review
    ModerationQueue.objects.create(
        listing=listing,
        reason=f"New listing - Spam score: {spam_score}" if spam_score > 0 else "New listing awaiting review",
        status='pending'
    )
    
    return listing
