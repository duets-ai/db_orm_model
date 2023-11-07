from rest_framework import serializers
from .models import *
import re


class Utils:
    @staticmethod
    def extract_name(s):
        match = re.search(r'(- )(.+)', s)
        return match.group(1) if match else None


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


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'uuid',
            'zoom_user_id',
            'full_name',
            'email',
            'is_teacher',
            'native_language',
            'target_language',
        )
        model = User


class MeetingSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    meeting_recordings = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'uuid',
            'zoom_meeting_uuid',
            'start_time',
            'end_time',
            'host',
            'languages',
            'participants',
            'meeting_recordings',
            'transcription_blob',
        )
        model = Meeting

    def get_participants(self, obj):
        participants_uuids = MeetingParticipants.objects.filter(meeting=obj.zoom_meeting_uuid).values_list('user',
                                                                                                           flat=True)
        participants = User.objects.filter(zoom_user_id__in=participants_uuids)
        return ParticipantSerializer(participants, many=True).data

    def get_meeting_recordings(self, obj):
        recordings = MeetingRecordings.objects.filter(meeting=obj.zoom_meeting_uuid)
        return MeetingRecordingSerializer(recordings, many=True).data


class MeetingParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingParticipants
        fields = ['meeting', 'user']

    def validate(self, data):
        # Check if the user is already a participant
        if MeetingParticipants.objects.filter(meeting=data['meeting'], user=data['user']).exists():
            raise serializers.ValidationError("The user is already a participant of the meeting.")
        return data


class MeetingRecordingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = MeetingRecordings
        fields = ['meeting', 'file_id', 'file_name', 'file_type', 'file_size', 'download_url', 'download_token', 'user']

    def get_user(self, obj):
        file_name = obj.file_name
        user_name = Utils.extract_name(file_name)
        try:
            user = User.objects.get(full_name=user_name)
        except User.DoesNotExist:
            return None
        return ParticipantSerializer(user).data

    def validate(self, data):
        # Check if the file is already a recording
        if MeetingRecordings.objects.filter(meeting=data['meeting'], file_id=data['file_id']).exists():
            raise serializers.ValidationError("The file is already a recording of the meeting.")
        return data
