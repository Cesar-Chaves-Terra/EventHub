from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from events.models import Event, OrganizerProfile
from participants.models import Participant, Registration


class RegistrationSeatSignalTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="organizer_test",
            password="test-password",
        )
        organizer = OrganizerProfile.objects.create(user=user)

        self.event = Event.objects.create(
            name="Signal Test Event",
            description="Event for signal tests",
            date="2026-11-20T14:00:00Z",
            capacity=2,
            available_seats=2,
            organizer=organizer,
        )

        self.participant = Participant.objects.create(
            name="Test Participant",
            email="participant@example.com",
        )

    def create_registration(self):
        return Registration.objects.create(
            event=self.event,
            participant=self.participant,
            status="ACTIVE",
        )

    def test_active_registration_decreases_available_seats(self):
        self.create_registration()

        self.event.refresh_from_db()
        self.assertEqual(self.event.available_seats, 1)

    def test_cancelling_registration_restores_available_seat(self):
        registration = self.create_registration()

        registration.status = "CANCELLED"
        registration.save()

        self.event.refresh_from_db()
        self.assertEqual(self.event.available_seats, 2)

    def test_reactivating_registration_decreases_available_seat(self):
        registration = self.create_registration()
        registration.status = "CANCELLED"
        registration.save()

        registration.status = "ACTIVE"
        registration.save()

        self.event.refresh_from_db()
        self.assertEqual(self.event.available_seats, 1)

    def test_saving_without_status_change_does_not_change_seats(self):
        registration = self.create_registration()
        registration.save()

        self.event.refresh_from_db()
        self.assertEqual(self.event.available_seats, 1)

    def test_deleting_active_registration_restores_seat(self):
        registration = self.create_registration()
        registration.delete()

        self.event.refresh_from_db()
        self.assertEqual(self.event.available_seats, 2)

    def test_registration_fails_when_event_has_no_seats(self):
        self.event.available_seats = 0
        self.event.save(update_fields=["available_seats"])

        with self.assertRaises(ValidationError):
            self.create_registration()

        self.assertEqual(
            Registration.objects.filter(event=self.event).count(),
            0,
        )

        self.event.refresh_from_db()
        self.assertEqual(self.event.available_seats, 0)

