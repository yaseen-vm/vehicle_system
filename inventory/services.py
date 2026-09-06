from decimal import Decimal
from django.db import transaction
from .models import Booking, Vehicle

class VehicleUnavailableError(Exception):
    pass

class BookingOverlapError(Exception):
    pass

class BookingService:
    @staticmethod
    @transaction.atomic
    def create_booking(*, vehicle, customer_name, customer_phone, start_date, end_date):
        vehicle = Vehicle.objects.select_for_update().get(pk=vehicle.pk)
        if not vehicle.is_available:
            raise VehicleUnavailableError
        if Booking.objects.filter(vehicle_id=vehicle.id, start_date__lt=end_date, end_date__gt=start_date).exists():
            raise BookingOverlapError
        days = (end_date - start_date).days
        total_amount = Decimal(days) * vehicle.price_per_day
        booking = Booking.objects.create(vehicle=vehicle, customer_name=customer_name, customer_phone=customer_phone, start_date=start_date, end_date=end_date, total_amount=total_amount)
        vehicle.is_available = False
        vehicle.save(update_fields=["is_available"])
        return booking
