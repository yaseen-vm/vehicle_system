from django.db import migrations

CREATE_EXTENSION = "CREATE EXTENSION IF NOT EXISTS btree_gist;"
CREATE_CONSTRAINT = """
ALTER TABLE inventory_booking
ADD CONSTRAINT booking_no_overlapping_dates
EXCLUDE USING gist (
    vehicle_id WITH =,
    daterange(start_date, end_date, '[)') WITH &&
);
"""
DROP_CONSTRAINT = "ALTER TABLE inventory_booking DROP CONSTRAINT IF EXISTS booking_no_overlapping_dates;"

def add_constraint(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(CREATE_EXTENSION)
        cursor.execute(CREATE_CONSTRAINT)

def remove_constraint(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(DROP_CONSTRAINT)

class Migration(migrations.Migration):
    dependencies = [("inventory", "0001_initial")]
    operations = [migrations.RunPython(add_constraint, remove_constraint)]
