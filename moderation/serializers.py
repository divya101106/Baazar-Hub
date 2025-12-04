from rest_framework import serializers
from .models import ModerationQueue
from listings.serializers import ListingSerializer

class ModerationQueueSerializer(serializers.ModelSerializer):
    listing_details = ListingSerializer(source='listing', read_only=True)

    class Meta:
        model = ModerationQueue
        fields = ['id', 'listing', 'listing_details', 'reason', 'status', 'created_at', 'reviewed_at']
        read_only_fields = ['created_at', 'reviewed_at']
