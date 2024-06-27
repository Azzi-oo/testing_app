from rest_framework.routers import SimpleRouter
from general.api.views import RoomViewSet, BookingViewSet


router = SimpleRouter()
router.register(r'rooms', RoomViewSet, basename="users")
router.register(r'posts', BookingViewSet, basename="posts")


urlpatterns = router.urls
