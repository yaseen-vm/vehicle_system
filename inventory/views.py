from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from .filters import VehicleFilter
from .models import Booking, Vehicle
from .serializers import BookingSerializer, VehicleSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = VehicleFilter

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.select_related("vehicle").all()
    serializer_class = BookingSerializer

class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.select_related("vehicle").all()
    serializer_class = BookingSerializer
