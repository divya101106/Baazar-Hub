from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source='sender.username')
    receiver_name = serializers.ReadOnlyField(source='receiver.username')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'receiver', 'receiver_name', 'offer', 'content', 'timestamp', 'is_read']
        read_only_fields = ['sender', 'timestamp', 'is_read']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)
