from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'id', 'restaurant', 'reservation_time', 'number_of_guests',
            'duration', 'special_requests', 'created_at', 'canceled', 'table'
        ]
        read_only_fields = ['id', 'customer', 'table', 'created_at' 'canceled']