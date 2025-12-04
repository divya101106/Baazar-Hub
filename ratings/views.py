from rest_framework import viewsets, permissions
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Rating
from .serializers import RatingSerializer
from offers.models import Offer

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Users can only see ratings they gave or received
        user = self.request.user
        if user.is_authenticated:
            return Rating.objects.filter(
                Q(rater=user) | Q(rated_user=user)
            )
        # For unauthenticated, show all ratings
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Rating.objects.filter(rated_user_id=user_id)
        return Rating.objects.all()

    def perform_create(self, serializer):
        # Validate that user is involved in the transaction
        transaction = serializer.validated_data.get('transaction')
        rated_user = serializer.validated_data.get('rated_user')
        
        if transaction:
            # Verify user is buyer or seller in this transaction
            if self.request.user != transaction.buyer and self.request.user != transaction.listing.seller:
                raise permissions.PermissionDenied("You can only rate users involved in your transactions.")
            
            # Verify transaction is accepted
            if transaction.status != 'accepted':
                raise permissions.PermissionDenied("You can only rate users after an accepted transaction.")
        else:
            # If no transaction, check if users have any accepted offers together
            has_transaction = Offer.objects.filter(
                Q(status='accepted') &
                (Q(buyer=self.request.user, listing__seller=rated_user) |
                 Q(buyer=rated_user, listing__seller=self.request.user))
            ).exists()
            
            if not has_transaction:
                raise permissions.PermissionDenied("You can only rate users you have completed transactions with.")
        
        serializer.save(rater=self.request.user)

@login_required
def create_rating(request, user_id, offer_id=None):
    """Create a rating for a user after transaction"""
    rated_user = get_object_or_404(User, id=user_id)
    
    # Don't allow rating yourself
    if rated_user == request.user:
        messages.error(request, "You cannot rate yourself.")
        return redirect('home')
    
    # Verify transaction exists and is accepted
    if offer_id:
        offer = get_object_or_404(Offer, id=offer_id)
        # Verify user is involved
        if request.user != offer.buyer and request.user != offer.listing.seller:
            messages.error(request, "You don't have permission to rate this user.")
            return redirect('home')
        
        if offer.status != 'accepted':
            messages.error(request, "You can only rate after an accepted transaction.")
            return redirect('home')
    else:
        # Check if users have any accepted offers together
        offer = Offer.objects.filter(
            Q(status='accepted') &
            (Q(buyer=request.user, listing__seller=rated_user) |
             Q(buyer=rated_user, listing__seller=request.user))
        ).first()
        
        if not offer:
            messages.error(request, "You can only rate users you have completed transactions with.")
            return redirect('home')
    
    # Check if rating already exists
    existing_rating = Rating.objects.filter(
        rater=request.user,
        rated_user=rated_user,
        transaction=offer
    ).first()
    
    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        comment = request.POST.get('comment', '').strip()
        
        if score < 1 or score > 5:
            messages.error(request, "Rating must be between 1 and 5.")
        else:
            if existing_rating:
                existing_rating.score = score
                existing_rating.comment = comment
                existing_rating.save()
                messages.success(request, "Rating updated!")
            else:
                Rating.objects.create(
                    rater=request.user,
                    rated_user=rated_user,
                    transaction=offer,
                    score=score,
                    comment=comment
                )
                messages.success(request, "Rating submitted!")
            return redirect('user_profile_detail', user_id=user_id)
    
    return render(request, 'ratings/create_rating.html', {
        'rated_user': rated_user,
        'offer': offer,
        'existing_rating': existing_rating
    })
