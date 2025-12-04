import os
from django.core.exceptions import ValidationError

# Try to import Pillow, but handle gracefully if not installed
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

ALLOWED_IMAGE_TYPES = ['JPEG', 'PNG', 'JPG']
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_IMAGES_PER_LISTING = 5

def validate_image_file(image):
    """
    Validate a single image file.
    Returns (is_valid, error_message)
    """
    if not image:
        return False, "No image provided"
    
    # Check file size
    if image.size > MAX_IMAGE_SIZE:
        return False, f"Image size exceeds {MAX_IMAGE_SIZE / (1024*1024):.1f}MB limit"
    
    # Check file extension
    ext = os.path.splitext(image.name)[1].upper().replace('.', '')
    if ext not in ALLOWED_IMAGE_TYPES:
        return False, f"Invalid file type. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
    
    # Try to open and validate with Pillow if available
    if PILLOW_AVAILABLE:
        try:
            # Reset file pointer
            image.seek(0)
            img = Image.open(image)
            img.verify()
            
            # Reset file pointer again after verify
            image.seek(0)
            
            # Check if it's a valid image format
            if img.format not in ['JPEG', 'PNG']:
                return False, "Invalid image format. Only JPEG and PNG are allowed"
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    else:
        # If Pillow is not available, just check extension
        # This is a basic validation - for production, Pillow should be installed
        pass
    
    return True, None

def validate_images(images, max_count=MAX_IMAGES_PER_LISTING):
    """
    Validate multiple image files.
    Returns (is_valid, error_message, valid_images)
    """
    if not images:
        return True, None, []
    
    if len(images) > max_count:
        return False, f"Maximum {max_count} images allowed per listing", []
    
    valid_images = []
    for idx, image in enumerate(images):
        is_valid, error = validate_image_file(image)
        if not is_valid:
            return False, f"Image {idx + 1}: {error}", []
        valid_images.append(image)
    
    return True, None, valid_images

