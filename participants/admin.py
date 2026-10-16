
from django.contrib import admin

from .models import Participant, Registration


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone_number",
        "registration_date",
    )
    search_fields = ("name", "email")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "participant",
        "event",
        "status",
        "registration_date",
    )
    search_fields = (
        "participant__name",
        "participant__email",
        "event__name",
    )
    list_filter = ("status", "registration_date")
