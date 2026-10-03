from rest_framework.routers import DefaultRouter

from .views import EventViewSet


router = DefaultRouter()
router.register("events", EventViewSet, basename="event")

urlpatterns = router.urls


#URL de acesso: 
# GET     /api/events/
#POST    /api/events/
#GET     /api/events/1/
#PUT     /api/events/1/
#PATCH   /api/events/1/
#DELETE  /api/events/1/