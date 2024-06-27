from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from general.models import Room, Booking
from datetime import date


class RoomViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser('admin', 'admin@yandex.ru', 'password')
        self.user = User.objects.create_user('user', 'user@yandex.ru', 'pass')
        self.room1 = Room.objects.create(name='Room 1', price_per_night=100, capacity=1)
        self.room2 = Room.objects.create(name='Room 2', price_per_night=150, capacity=2)

    def test_list_rooms(self):
        response = self.client.get(reverse('room-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_rooms_by_price(self):
        response = self.client.get(reverse('room-list'), {'ordering': 'price_per_night'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Room 1')


# class BookingViewSetTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.
