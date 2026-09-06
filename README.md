# Vehicle Inventory & Booking API

Production-oriented Django REST API for vehicle inventory and booking management.

## Stack
- Django 5.2
- Django REST Framework
- django-filter
- drf-spectacular / Swagger
- SQLite for local development
- PostgreSQL recommended for production

## Architecture
`View/ViewSet → Serializer → BookingService → Django ORM → Database constraints/indexes`

Booking creation is transactional and locks the vehicle row with `select_for_update()`. PostgreSQL additionally uses a GiST exclusion constraint to prevent overlapping bookings for the same vehicle.

## API

### Vehicles
- `GET /api/vehicles/`
- `POST /api/vehicles/`
- `GET /api/vehicles/<id>/`
- `PUT /api/vehicles/<id>/`
- `PATCH /api/vehicles/<id>/`
- `DELETE /api/vehicles/<id>/`

### Bookings
- `GET /api/bookings/`
- `POST /api/bookings/`
- `GET /api/bookings/<id>/`

### Filters
`GET /api/vehicles/?brand=Toyota&fuel_type=Hybrid&is_available=true`

Brand filtering is case-insensitive.

## Booking rules
- Start date cannot be in the past.
- End date must be after start date.
- Customer phone must contain exactly 10 digits.
- Overlapping bookings for the same vehicle are rejected.
- `total_amount` is calculated server-side as `(end_date - start_date).days × price_per_day`.
- A successfully booked vehicle becomes unavailable.
- Database check constraints enforce row-level integrity.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API base: `http://127.0.0.1:8000/api/`

Swagger: `http://127.0.0.1:8000/api/docs/`

OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Test

```bash
python manage.py test
python manage.py check --deploy
```

## Production

Use PostgreSQL and set `DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS`, and PostgreSQL environment variables. Run migrations and collect static files before serving with Gunicorn:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn vehicle_system.wsgi:application
```

See `.env.example` for configuration.
