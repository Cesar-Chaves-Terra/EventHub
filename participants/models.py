from django.db import models

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Registration(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("CANCELLED", "Cancelled"),
    ]

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    participant = models.ForeignKey(
        "participants.Participant",
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    registration_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ACTIVE",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "participant"],
                name="unique_event_participant_registration",
            )
        ]

    def __str__(self):
        return f"{self.participant.name} - {self.event.name}"