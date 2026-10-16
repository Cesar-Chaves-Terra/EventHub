
from django.db.models import Count
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "registration_counts"]:
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        organizer = self.request.user.organizer_profile
        serializer.save(organizer=organizer)

    @action(detail=False, methods=["get"], url_path="registration-counts")
    def registration_counts(self, request):
        events = Event.objects.annotate(
            registration_count=Count("registrations")
        ).values("id", "name", "registration_count")

        return Response(events)
