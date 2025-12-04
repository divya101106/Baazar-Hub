from rest_framework import serializers
from .models import Offer

class OfferSerializer(serializers.ModelSerializer):
    buyer_name = serializers.ReadOnlyField(source='buyer.username')
    listing_title = serializers.ReadOnlyField(source='listing.title')

    class Meta:
        model = Offer
        fields = ['id', 'buyer', 'buyer_name', 'listing', 'listing_title', 'amount', 'status', 'created_at']
        read_only_fields = ['buyer', 'status', 'created_at']

    def create(self, validated_data):
        validated_data['buyer'] = self.context['request'].user
        return super().create(validated_data)
