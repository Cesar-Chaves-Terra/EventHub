from django.db import models


class EventManager(models.Manager):
    def available(self):
        return self.filter(available_seats__gt=0)