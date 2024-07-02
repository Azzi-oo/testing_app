from django_filters import rest_framework as filters
from general.models import Room, Booking


class RoomFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='booking__start_date', lookup_expr='lt', exclude=True)
    end_date = filters.DateFilter(field_name='booking__end_date', lookup_expr='gt', exclude=True)

    class Meta:
        model = Room
        fields = ['name', 'price_per_night', 'capacity']


class BookingFilter(filters.FilterSet):
    class Meta:
        model = Booking
        fields = ['user', 'start_date', 'end_date']
