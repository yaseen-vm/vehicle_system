from datetime import date
from rest_framework import serializers
from .models import Booking, Vehicle
from .services import BookingOverlapError, BookingService, VehicleUnavailableError

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ("id", "name", "brand", "year", "price_per_day", "fuel_type", "is_available")

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "vehicle", "customer_name", "customer_phone", "start_date", "end_date", "total_amount")
        read_only_fields = ("id", "total_amount")

    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value

    def validate(self, attrs):
        if attrs.get("start_date") and attrs.get("end_date") and attrs["end_date"] <= attrs["start_date"]:
            raise serializers.ValidationError({"end_date": "End date must be after start date."})
        return attrs

    def create(self, validated_data):
        try:
            return BookingService.create_booking(**validated_data)
        except VehicleUnavailableError as exc:
            raise serializers.ValidationError({"vehicle": "This vehicle is currently unavailable."}) from exc
        except BookingOverlapError as exc:
            raise serializers.ValidationError({"vehicle": "This vehicle is already booked for an overlapping date range."}) from exc
