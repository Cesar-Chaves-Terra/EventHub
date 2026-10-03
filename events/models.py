from django.contrib.auth.models import User
from django.db import models


class OrganizerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="organizer_profile",
    )

    def __str__(self):
        return self.user.username