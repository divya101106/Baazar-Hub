from rest_framework import serializers
from .models import Listing, ListingImage, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'uploaded_at']

class MultipleImageField(serializers.Field):
    """Custom field to handle multiple image uploads"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Try to make it render as a file input in HTML forms
        self.style = {'base_template': 'input.html', 'input_type': 'file'}
    
    def to_internal_value(self, data):
        # For HTML forms, images are handled via request.FILES in the view
        # For API calls, this should receive a list of file objects
        if not data:
            return []
        # Handle both single file and list of files
        if isinstance(data, list):
            return data
        # If it's a single file object, wrap it in a list
        return [data] if data else []
    
    def to_representation(self, value):
        # Write-only field, shouldn't be in representation
        return None

class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    uploaded_images = MultipleImageField(
        write_only=True,
        required=False,
        allow_null=True
    )
    seller_name = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'price', 'category', 'seller', 'seller_name', 'status', 'created_at', 'images', 'uploaded_images']
        read_only_fields = ['seller', 'status', 'created_at', 'flags']

    def validate_title(self, value):
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Title must be at least 10 characters long")
        return value.strip()

    def validate_description(self, value):
        if not value or len(value.strip()) < 50:
            raise serializers.ValidationError("Description must be at least 50 characters long")
        return value.strip()

    def validate_price(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value

    def validate_uploaded_images(self, value):
        # Allow empty or None for HTML forms (images handled via request.FILES in view)
        return value or []
    
    def to_representation(self, instance):
        """Override to exclude uploaded_images from response"""
        ret = super().to_representation(instance)
        # uploaded_images is write_only, so it won't appear anyway, but ensure it's not there
        ret.pop('uploaded_images', None)
        return ret
