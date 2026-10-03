from django.contrib.auth.models import User
from django.db import models

from .managers import EventManager


class OrganizerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="organizer_profile",
    )

    def __str__(self):
        return self.user.username


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    organizer = models.ForeignKey(
        OrganizerProfile,
        on_delete=models.CASCADE,
        related_name="events",
    )

    objects = EventManager()

    def __str__(self):
        return self.name