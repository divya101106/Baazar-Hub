from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from offers.models import Offer
from ratings.models import Rating
from .forms import CustomUserCreationForm, EditProfileForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def custom_login(request):
    """
    Custom login view that provides specific error messages for wrong username vs wrong password.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        error_message = None
        error_type = None  # 'username' or 'password'
        
        if not username:
            error_message = "Please enter your username."
            error_type = 'username'
        elif not password:
            error_message = "Please enter your password."
            error_type = 'password'
        else:
            # Check if username exists
            try:
                user = User.objects.get(username=username)
                # Username exists, now check password
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    # Login successful
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('home')
                else:
                    # Password is incorrect
                    error_message = "Password is incorrect. Please try again."
                    error_type = 'password'
            except User.DoesNotExist:
                # Username doesn't exist
                error_message = "Username is incorrect. Please check your username and try again."
                error_type = 'username'
        
        # Render form with error
        return render(request, 'users/login.html', {
            'error_message': error_message,
            'error_type': error_type,
            'username': username,  # Preserve username on error
        })
    
    # GET request - show login form
    return render(request, 'users/login.html')

@login_required
def edit_profile(request):
    """Edit user profile information"""
    user = request.user
    # Ensure user has a profile
    from .models import UserProfile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user, user=user)
        if form.is_valid():
            # Save user data
            user = form.save()
            # Update phone number in profile
            phone_number = form.cleaned_data.get('phone_number', '')
            profile.phone_number = phone_number
            profile.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-populate form with current user data
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'phone_number': profile.phone_number if profile.phone_number and profile.phone_number != '0000000000' else '',
        }
        form = EditProfileForm(instance=user, initial=initial_data, user=user)
    
    return render(request, 'users/edit_profile.html', {'form': form})

def user_profile(request, user_id=None):
    """Display user profile with listings, offers, and ratings"""
    # If no user_id provided, show current user's profile
    if user_id:
        profile_user = get_object_or_404(User, id=user_id)
    else:
        profile_user = request.user
        if not request.user.is_authenticated:
            return redirect('login')
    
    # Ensure user has a profile (create if doesn't exist)
    from .models import UserProfile
    UserProfile.objects.get_or_create(user=profile_user)
    
    # Get user's listings (as seller)
    listings = Listing.objects.filter(seller=profile_user).select_related('category').prefetch_related('images').order_by('-created_at')
    
    # Get user's offers (as buyer)
    offers_made = Offer.objects.filter(buyer=profile_user).select_related('listing', 'listing__seller').order_by('-created_at')
    
    # Get offers received (as seller)
    offers_received = Offer.objects.filter(listing__seller=profile_user).select_related('buyer', 'listing').order_by('-created_at')
    
    # Get ratings received
    ratings_received = Rating.objects.filter(rated_user=profile_user).select_related('rater', 'transaction').order_by('-created_at')
    
    # Get ratings given
    ratings_given = Rating.objects.filter(rater=profile_user).select_related('rated_user', 'transaction').order_by('-created_at')
    
    # Calculate average rating
    if ratings_received.exists():
        avg_rating = sum(r.score for r in ratings_received) / ratings_received.count()
    else:
        avg_rating = 0
    
    # Count statistics
    stats = {
        'total_listings': listings.count(),
        'active_listings': listings.filter(status='approved').count(),
        'total_offers_made': offers_made.count(),
        'accepted_offers': offers_made.filter(status='accepted').count(),
        'total_ratings': ratings_received.count(),
        'average_rating': round(avg_rating, 1) if avg_rating > 0 else 0,
    }
    
    context = {
        'profile_user': profile_user,
        'listings': listings[:6],  # Show first 6 listings
        'all_listings_count': listings.count(),
        'offers_made': offers_made[:5],  # Show first 5 offers
        'offers_received': offers_received[:5],  # Show first 5 offers received
        'ratings_received': ratings_received[:5],  # Show first 5 ratings
        'ratings_given': ratings_given[:5],  # Show first 5 ratings given
        'stats': stats,
        'is_own_profile': request.user == profile_user if request.user.is_authenticated else False,
    }
    
    return render(request, 'users/profile.html', context)
