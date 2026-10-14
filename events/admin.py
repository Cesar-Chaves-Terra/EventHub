from django.contrib import admin

from .models import Event, OrganizerProfile

@admin.register(OrganizerProfile)
class OrganizerProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user_name", "user_email")

    @admin.register(Event)
    class EventAdmin(admin.ModelAdmin):
        list_display = (
            "name",
            "date",
            "organizer",
            "capacity",
            "available_seats",
            )
        search_fields = ("name", "description")
        list_filter = ("date",)