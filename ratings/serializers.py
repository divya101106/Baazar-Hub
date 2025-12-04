from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    rater_name = serializers.ReadOnlyField(source='rater.username')
    rated_user_name = serializers.ReadOnlyField(source='rated_user.username')

    class Meta:
        model = Rating
        fields = ['id', 'rater', 'rater_name', 'rated_user', 'rated_user_name', 'transaction', 'score', 'comment', 'created_at']
        read_only_fields = ['rater', 'created_at']

    def create(self, validated_data):
        validated_data['rater'] = self.context['request'].user
        return super().create(validated_data)
