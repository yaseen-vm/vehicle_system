import json
import urllib.request
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000/api"

def request(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE_URL + path, data=data, headers={"Content-Type":"application/json"}, method=method)
    with urllib.request.urlopen(req) as response:
        body = response.read().decode()
        return response.status, json.loads(body) if body else {}

if __name__ == "__main__":
    status, vehicle = request("POST", "/vehicles/", {"name":"Smoke Test Car","brand":"Toyota","year":2024,"price_per_day":"50.00","fuel_type":"Hybrid","is_available":True})
    print("Create vehicle:", status, vehicle)
    start = date.today() + timedelta(days=2)
    end = start + timedelta(days=3)
    status, booking = request("POST", "/bookings/", {"vehicle":vehicle["id"],"customer_name":"Smoke Tester","customer_phone":"9876543210","start_date":start.isoformat(),"end_date":end.isoformat()})
    print("Create booking:", status, booking)
