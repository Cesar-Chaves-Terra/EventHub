from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from events.models import Event
from participants.models import Registration


@receiver(pre_save, sender=Registration)
def track_previous_registration_status(sender, instance, **kwargs):
    if instance._state.adding:
        instance._previous_status = None
        return

    instance._previous_status = (
        Registration.objects.filter(pk=instance.pk)
        .values_list("status", flat=True)
        .first()
    )


@receiver(post_save, sender=Registration)
def update_event_seats_on_registration_save(
    sender, instance, created, **kwargs
):
    previous_status = getattr(instance, "_previous_status", None)

    became_active = (
        instance.status == "ACTIVE"
        and (created or previous_status == "CANCELLED")
    )

    became_cancelled = (
        not created
        and previous_status == "ACTIVE"
        and instance.status == "CANCELLED"
    )

    if not became_active and not became_cancelled:
        return

    with transaction.atomic():
        if became_active:
            updated = Event.objects.filter(
                pk=instance.event_id,
                available_seats__gt=0,
            ).update(
                available_seats=F("available_seats") - 1
            )

            if updated == 0:
                raise ValidationError(
                    "This event has no available seats."
                )

        elif became_cancelled:
            Event.objects.filter(
                pk=instance.event_id,
                available_seats__lt=F("capacity"),
            ).update(
                available_seats=F("available_seats") + 1
            )


@receiver(post_delete, sender=Registration)
def restore_event_seat_on_registration_delete(
    sender, instance, **kwargs
):
    if instance.status != "ACTIVE":
        return

    with transaction.atomic():
        Event.objects.filter(
            pk=instance.event_id,
            available_seats__lt=F("capacity"),
        ).update(
            available_seats=F("available_seats") + 1
        )
