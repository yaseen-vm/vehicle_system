from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q

phone_validator = RegexValidator(regex=r"^\d{10}$", message="Phone number must contain exactly 10 digits.")

class Vehicle(models.Model):
    class FuelType(models.TextChoices):
        PETROL = "Petrol", "Petrol"
        DIESEL = "Diesel", "Diesel"
        ELECTRIC = "Electric", "Electric"
        HYBRID = "Hybrid", "Hybrid"

    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=120)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1886), MaxValueValidator(2100)])
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(condition=Q(year__gte=1886) & Q(year__lte=2100), name="vehicle_year_valid"),
            models.CheckConstraint(condition=Q(price_per_day__gt=0), name="vehicle_price_positive"),
        ]
        indexes = [
            models.Index(fields=["brand"], name="vehicle_brand_idx"),
            models.Index(fields=["fuel_type"], name="vehicle_fuel_type_idx"),
            models.Index(fields=["is_available"], name="vehicle_available_idx"),
        ]

    def __str__(self):
        return f"{self.brand} {self.name} ({self.year})"

class Booking(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="bookings")
    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=10, validators=[phone_validator])
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ["-start_date", "-id"]
        constraints = [
            models.CheckConstraint(condition=Q(end_date__gt=models.F("start_date")), name="booking_end_after_start"),
            models.CheckConstraint(condition=Q(total_amount__gt=0), name="booking_total_positive"),
            models.CheckConstraint(condition=Q(customer_phone__regex=r"^\d{10}$"), name="booking_phone_ten_digits"),
        ]
        indexes = [models.Index(fields=["vehicle", "start_date", "end_date"], name="booking_vehicle_dates_idx")]

    def __str__(self):
        return f"{self.customer_name} - {self.vehicle}"
