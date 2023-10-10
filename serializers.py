from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'uuid',
            'full_name',
            'email',
            'is_teacher',
            'native_language',
            'target_language',
            'zoom_access_token',
            'zoom_refresh_token',
            'zoom_token_expiration',
            'zoom_user_id',
            'is_zoom_authenticated',
        )
        model = User


class MeetingSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    class Meta:
        fields = (
            'start_time',
            'end_time',
            'uuid',
            'zoom_meeting_uuid',
            'transcription_id',
            'participants',
            'host'
        )
        model = Meeting

    def get_participants(self, obj):
        participants_uuids = MeetingParticipant.objects.filter(meeting=obj.uuid).values_list('user', flat=True)
        participants = User.objects.filter(uuid__in=participants_uuids)
        return UserSerializer(participants, many=True).data

class MeetingParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingParticipants
        fields = ['meeting', 'user']

    def validate(self, data):
        # Check if the user is already a participant
        if MeetingParticipants.objects.filter(meeting=data['meeting'], user=data['user']).exists():
            raise serializers.ValidationError("The user is already a participant of the meeting.")
        return data

