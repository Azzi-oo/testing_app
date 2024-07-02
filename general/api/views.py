from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from general.api.filter import BookingFilter
from general.models import Room, Booking, User
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RoomSerializer, BookingSerializer, UserRegistrationSerializer
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['price_per_night', 'capacity']
    search_classses = ['name']


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookingFilter

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def available_rooms(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            booked_rooms = Booking.objects.filter(
                start_date__lt=end_date, end_date__gt=start_date
            ).values_list('room_id', flat=True)
            rooms = Room.objects.exclude(id__in=booked_rooms)
            serializer = RoomSerializer(rooms, many=True)
            return Response(serializer.data)
        return Response({'error': 'Please provide start_date and end_date'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        if request.user == booking.user or request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        return Response({'error': 'You do not have permission to cancel this booking'}, status=status.HTTP_403_FORBIDDEN)


class UserViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    queryset = User.objects.all().order_by("-id")

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        # return UserListSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
