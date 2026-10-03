from rest_framework import serializers

from .models import Participant, Registration


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "registration_date",
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    participant = serializers.PrimaryKeyRelatedField(
        queryset=Participant.objects.all()
    )
    participant_details = ParticipantSerializer(
        source="participant",
        read_only=True,
    )

    class Meta:
        model = Registration
        fields = [
            "id",
            "event",
            "participant",
            "participant_details",
            "registration_date",
            "status",
        ]