# Image Upload Guide for Classifieds Marketplace

## How Users Upload Images When Creating Listings

### Method 1: HTML Form (Web Interface)

1. **Navigate to Create Listing Page**
   - URL: `/create-listing/` or `/listings/create/`
   - User must be logged in

2. **Fill in Listing Details (Step 1)**
   - Title (minimum 10 characters)
   - Category (select from dropdown)
   - Price (must be greater than 0)
   - Description (minimum 50 characters)

3. **Upload Images (Step 2)**
   - Click "Choose Files" button or drag and drop images
   - Select up to 5 images
   - Supported formats: JPEG, JPG, PNG
   - Maximum file size: 5MB per image
   - Images are validated on the client side before submission

4. **Review and Submit (Step 3)**
   - Review all information
   - Click "Submit Listing"
   - Images are uploaded along with the form data

### Method 2: REST API

**Endpoint:** `POST /api/listings/`

**Request Format:**
- Content-Type: `multipart/form-data`
- Fields:
  - `title`: string (required, min 10 chars)
  - `description`: string (required, min 50 chars)
  - `price`: decimal (required, > 0)
  - `category`: integer (category ID)
  - `uploaded_images`: array of image files (optional, max 5)

**Example using curl:**
```bash
curl -X POST http://localhost:8000/api/listings/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "title=iPhone 13 Pro Max" \
  -F "description=Great condition iPhone with 256GB storage" \
  -F "price=800.00" \
  -F "category=1" \
  -F "uploaded_images=@image1.jpg" \
  -F "uploaded_images=@image2.jpg"
```

**Example using Python requests:**
```python
import requests

url = "http://localhost:8000/api/listings/"
headers = {"Authorization": "Token YOUR_TOKEN"}
files = [
    ('uploaded_images', open('image1.jpg', 'rb')),
    ('uploaded_images', open('image2.jpg', 'rb'))
]
data = {
    'title': 'iPhone 13 Pro Max',
    'description': 'Great condition iPhone with 256GB storage',
    'price': '800.00',
    'category': 1
}
response = requests.post(url, headers=headers, files=files, data=data)
```

## Image Validation Rules

### Client-Side Validation (HTML Form)
- Maximum 5 images per listing
- Only JPEG, JPG, PNG formats allowed
- Maximum 5MB per image
- Validation happens before form submission

### Server-Side Validation
- File type validation (JPEG, PNG only)
- File size validation (max 5MB)
- Image format verification using Pillow (if installed)
- Maximum 5 images enforced
- Image safety checks (basic validation)

## Image Storage

- Images are stored in: `media/listings/`
- Each image is associated with a `ListingImage` model
- Images are linked to listings via foreign key relationship
- Images are accessible via: `/media/listings/filename.jpg`

## Error Handling

If image upload fails, users will see:
- **Client-side**: Alert messages for validation errors
- **Server-side**: Error messages returned in the response
- **Form errors**: Displayed in the form if validation fails

## Technical Details

### Backend Processing Flow:
1. Form/API receives listing data + images
2. Images extracted from `request.FILES`
3. Images validated using `utils.image_validation.validate_images()`
4. Listing created via `services.listings_service.create_listing()`
5. Images saved as `ListingImage` objects
6. Moderation checks run (spam score, image safety)
7. Listing status set (approved/pending based on moderation)
8. Response returned with listing details

### Files Involved:
- `listings/views.py` - Handles form submission and API requests
- `listings/forms.py` - Form validation
- `listings/serializers.py` - API serialization
- `services/listings_service.py` - Business logic
- `utils/image_validation.py` - Image validation utilities
- `templates/listings/create.html` - HTML form template

