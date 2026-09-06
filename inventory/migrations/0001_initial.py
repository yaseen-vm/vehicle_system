from django.db import migrations, models
import django.db.models.deletion
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import Q, F

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Vehicle", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=120)), ("brand", models.CharField(max_length=120)),
            ("year", models.PositiveSmallIntegerField(validators=[MinValueValidator(1886), MaxValueValidator(2100)])),
            ("price_per_day", models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.01)])),
            ("fuel_type", models.CharField(choices=[("Petrol","Petrol"),("Diesel","Diesel"),("Electric","Electric"),("Hybrid","Hybrid")], max_length=20)),
            ("is_available", models.BooleanField(default=True)),], options={"ordering":["id"]}),
        migrations.CreateModel(name="Booking", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("customer_name", models.CharField(max_length=120)),
            ("customer_phone", models.CharField(max_length=10, validators=[RegexValidator(message="Phone number must contain exactly 10 digits.", regex="^\\d{10}$")])),
            ("start_date", models.DateField()), ("end_date", models.DateField()), ("total_amount", models.DecimalField(decimal_places=2, max_digits=12)),
            ("vehicle", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bookings", to="inventory.vehicle")),], options={"ordering":["-start_date","-id"]}),
        migrations.AddConstraint(model_name="vehicle", constraint=models.CheckConstraint(condition=Q(year__gte=1886) & Q(year__lte=2100), name="vehicle_year_valid")),
        migrations.AddConstraint(model_name="vehicle", constraint=models.CheckConstraint(condition=Q(price_per_day__gt=0), name="vehicle_price_positive")),
        migrations.AddConstraint(model_name="booking", constraint=models.CheckConstraint(condition=Q(end_date__gt=F("start_date")), name="booking_end_after_start")),
        migrations.AddConstraint(model_name="booking", constraint=models.CheckConstraint(condition=Q(total_amount__gt=0), name="booking_total_positive")),
        migrations.AddConstraint(model_name="booking", constraint=models.CheckConstraint(condition=Q(customer_phone__regex="^\\d{10}$"), name="booking_phone_ten_digits")),
        migrations.AddIndex(model_name="vehicle", index=models.Index(fields=["brand"], name="vehicle_brand_idx")),
        migrations.AddIndex(model_name="vehicle", index=models.Index(fields=["fuel_type"], name="vehicle_fuel_type_idx")),
        migrations.AddIndex(model_name="vehicle", index=models.Index(fields=["is_available"], name="vehicle_available_idx")),
        migrations.AddIndex(model_name="booking", index=models.Index(fields=["vehicle","start_date","end_date"], name="booking_vehicle_dates_idx")),
    ]
