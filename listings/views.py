from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Listing, Category, ListingImage
from .serializers import ListingSerializer, CategorySerializer
from .forms import ListingForm
from services.listings_service import create_listing as create_listing_service

def home(request):
    # Get search parameters
    search_query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    
    # Start with approved listings only
    listings = Listing.objects.filter(status='approved').select_related('category', 'seller').prefetch_related('images')
    
    # Filter by search query (product name/title)
    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    # Filter by category if selected
    if category_id:
        try:
            listings = listings.filter(category_id=int(category_id))
        except (ValueError, TypeError):
            pass  # Invalid category ID, ignore it
    
    # Order by creation date (newest first) and limit to 20 results
    listings = listings.order_by('-created_at')[:20]
    
    categories = Category.objects.all()
    
    # Determine if this is a search result
    is_search = bool(search_query or category_id)
    
    context = {
        'listings': listings,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'is_search': is_search,
    }
    
    return render(request, 'home.html', context)

@login_required
def create_listing_view(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                images = request.FILES.getlist('images')
                # Prepare data for service
                data = form.cleaned_data.copy()
                data['category_id'] = data['category'].id if data.get('category') else None
                
                # Use service to create listing
                listing = create_listing_service(request.user, data, images)
                from django.contrib import messages
                if listing.status == 'pending':
                    messages.success(request, 'Your listing has been submitted and is pending moderation review.')
                else:
                    messages.success(request, 'Your listing has been created successfully!')
                return redirect('home')
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'Error creating listing: {str(e)}')
        else:
            from django.contrib import messages
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ListingForm()
    return render(request, 'listings/create.html', {'form': form})

@login_required
def my_listings(request):
    """View all listings created by the current user"""
    user_listings = Listing.objects.filter(seller=request.user).select_related('category', 'seller').prefetch_related('images').order_by('-created_at')
    # Debug: Print to console (remove in production)
    print(f"User: {request.user.username}, Listings found: {user_listings.count()}")
    return render(request, 'listings/my_listings.html', {'listings': user_listings})

@login_required
def edit_listing(request, pk):
    """Edit an existing listing"""
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        
        # Handle image deletion
        if 'delete_images' in request.POST:
            image_ids_to_delete = request.POST.getlist('delete_images')
            ListingImage.objects.filter(id__in=image_ids_to_delete, listing=listing).delete()
            from django.contrib import messages
            messages.success(request, 'Images deleted successfully.')
            return redirect('edit_listing', pk=pk)
        
        if form.is_valid():
            try:
                # Update basic fields
                listing.title = form.cleaned_data['title']
                listing.description = form.cleaned_data['description']
                listing.price = form.cleaned_data['price']
                listing.category = form.cleaned_data['category']
                listing.save()
                
                # Handle new image uploads
                new_images = request.FILES.getlist('images')
                if new_images:
                    from utils.image_validation import validate_images
                    is_valid, error_msg, valid_images = validate_images(new_images, max_count=5 - listing.images.count())
                    if not is_valid:
                        from django.contrib import messages
                        messages.error(request, error_msg)
                        existing_images = listing.images.all()
                        return render(request, 'listings/edit.html', {
                            'form': form,
                            'listing': listing,
                            'existing_images': existing_images
                        })
                    
                    for image in valid_images:
                        ListingImage.objects.create(listing=listing, image=image)
                
                from django.contrib import messages
                messages.success(request, 'Listing updated successfully!')
                return redirect('my_listings')
            except Exception as e:
                import traceback
                print(f"Error updating listing: {str(e)}")
                print(traceback.format_exc())
                from django.contrib import messages
                messages.error(request, f'Error updating listing: {str(e)}')
                existing_images = listing.images.all()
                return render(request, 'listings/edit.html', {
                    'form': form,
                    'listing': listing,
                    'existing_images': existing_images
                })
        else:
            # Form has errors, show them on the edit page
            from django.contrib import messages
            messages.error(request, 'Please correct the errors in the form.')
            existing_images = listing.images.all()
            return render(request, 'listings/edit.html', {
                'form': form,
                'listing': listing,
                'existing_images': existing_images
            })
    else:
        form = ListingForm(instance=listing)
    
    existing_images = listing.images.all()
    return render(request, 'listings/edit.html', {
        'form': form,
        'listing': listing,
        'existing_images': existing_images
    })

def listing_detail(request, pk):
    try:
        listing = Listing.objects.select_related('seller', 'category').prefetch_related('images').get(pk=pk)
    except Listing.DoesNotExist:
        return render(request, '404.html', status=404) # Basic 404 handling
    
    # Check if user is authenticated and get related data
    context = {'listing': listing}
    
    if request.user.is_authenticated:
        from offers.models import Offer
        from ratings.models import Rating
        from cart.models import Cart
        
        # Check if user has an offer for this listing
        user_offer = Offer.objects.filter(
            buyer=request.user,
            listing=listing
        ).first()
        context['user_offer'] = user_offer
        
        # Check if user can rate the seller (has accepted transaction)
        can_rate = False
        rating_offer = None
        if request.user != listing.seller:
            rating_offer = Offer.objects.filter(
                Q(status='accepted', listing=listing) &
                (Q(buyer=request.user, listing__seller=listing.seller) |
                 Q(buyer=listing.seller, listing__seller=request.user))
            ).first()
            if rating_offer:
                can_rate = True
                # Check if rating already exists
                existing_rating = Rating.objects.filter(
                    rater=request.user,
                    rated_user=listing.seller,
                    transaction=rating_offer
                ).first()
                context['existing_rating'] = existing_rating
        
        context['can_rate'] = can_rate
        context['rating_offer'] = rating_offer
        
        # Check if item is in cart
        in_cart = Cart.objects.filter(user=request.user, listing=listing).exists()
        context['in_cart'] = in_cart
        
        # Check if user can chat (has an offer)
        can_chat = user_offer is not None or request.user == listing.seller
        context['can_chat'] = can_chat
        
    return render(request, 'listings/detail.html', context)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.filter(status='approved').order_by('-created_at')
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Use service layer for creation to handle moderation
        # We need to extract data and images manually because service expects them
        # But serializer.save() does it too. 
        # Let's override create method instead of perform_create to use the service fully
        pass

    def create(self, request, *args, **kwargs):
        # Handle images from request.FILES (works for both API and HTML form)
        images = []
        
        # Try to get images from request.FILES (for HTML forms and multipart API calls)
        if hasattr(request, 'FILES') and request.FILES:
            # Check for various possible field names
            for field_name in ['uploaded_images', 'uploaded_images[]', 'images']:
                if field_name in request.FILES:
                    uploaded_files = request.FILES.getlist(field_name)
                    if uploaded_files:
                        images = uploaded_files
                        break
        
        # Create a copy of request.data without files for serializer validation
        data = request.data.copy()
        # Remove image-related fields from data dict to avoid serializer confusion
        for key in ['uploaded_images', 'uploaded_images[]', 'images']:
            if key in data:
                data.pop(key)
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Extract data for service
        validated_data = serializer.validated_data.copy()
        
        # Convert category to category_id for service
        if 'category' in validated_data and validated_data['category']:
            validated_data['category_id'] = validated_data['category'].id
            validated_data.pop('category')
        
        # If no images from FILES, try to get from validated_data (for JSON API calls)
        if not images and 'uploaded_images' in serializer.validated_data:
            uploaded = serializer.validated_data.pop('uploaded_images', [])
            if uploaded:
                images = uploaded
        
        try:
            # Call service
            listing = create_listing_service(request.user, validated_data, images)
            
            # Return response
            headers = self.get_success_headers(serializer.data)
            return_serializer = ListingSerializer(listing)
            return Response(return_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            # Return proper error response
            return Response(
                {
                    'error': str(e),
                    'detail': 'Failed to create listing. Please check your input and try again.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset(self):
        # Allow sellers to see their own pending/rejected listings
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            my_listings = Listing.objects.filter(seller=self.request.user)
            queryset = queryset | my_listings
        return queryset.distinct()
