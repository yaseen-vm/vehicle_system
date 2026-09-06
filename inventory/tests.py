from datetime import date, timedelta
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Booking, Vehicle

class VehicleAPITests(TestCase):
    def setUp(self): self.client = APIClient()

    def test_create_vehicle(self):
        response = self.client.post("/api/vehicles/", {"name":"Model 3","brand":"Tesla","year":2024,"price_per_day":"100.00","fuel_type":"Electric","is_available":True}, format="json")
        self.assertEqual(response.status_code, 201)

    def test_vehicle_filtering(self):
        Vehicle.objects.create(name="Camry", brand="Toyota", year=2024, price_per_day="75.00", fuel_type="Petrol")
        Vehicle.objects.create(name="Model 3", brand="Tesla", year=2024, price_per_day="100.00", fuel_type="Electric")
        response = self.client.get("/api/vehicles/?brand=toyota")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

class BookingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vehicle = Vehicle.objects.create(name="Camry", brand="Toyota", year=2024, price_per_day=Decimal("75.00"), fuel_type="Petrol")

    def payload(self, **overrides):
        data = {"vehicle":self.vehicle.id,"customer_name":"John Doe","customer_phone":"9876543210","start_date":(date.today()+timedelta(days=2)).isoformat(),"end_date":(date.today()+timedelta(days=5)).isoformat()}
        data.update(overrides); return data

    def test_booking_calculates_total_and_disables_vehicle(self):
        response = self.client.post("/api/bookings/", self.payload(), format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["total_amount"], "225.00")
        self.vehicle.refresh_from_db(); self.assertFalse(self.vehicle.is_available)

    def test_client_cannot_override_total(self):
        response = self.client.post("/api/bookings/", self.payload(total_amount="1.00"), format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["total_amount"], "225.00")

    def test_past_start_date_rejected(self):
        response = self.client.post("/api/bookings/", self.payload(start_date=(date.today()-timedelta(days=1)).isoformat()), format="json")
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone_rejected(self):
        response = self.client.post("/api/bookings/", self.payload(customer_phone="12345"), format="json")
        self.assertEqual(response.status_code, 400)

    def test_overlap_rejected(self):
        start = date.today()+timedelta(days=2); end = date.today()+timedelta(days=5)
        Booking.objects.create(vehicle=self.vehicle, customer_name="Existing", customer_phone="9123456789", start_date=start, end_date=end, total_amount=Decimal("225.00"))
        response = self.client.post("/api/bookings/", self.payload(start_date=(date.today()+timedelta(days=3)).isoformat(), end_date=(date.today()+timedelta(days=6)).isoformat()), format="json")
        self.assertEqual(response.status_code, 400)
