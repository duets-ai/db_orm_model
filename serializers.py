from rest_framework import serializers
from .models import *
import re


class Utils:
    @staticmethod
    def extract_name(s):
        match = re.search(r'(- )(.+)', s)
        return match.group(2) if match else None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'uuid',
            'full_name',
            'hashed_password',
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
        extra_kwargs = {
            'email': {'required': True},
            'hashed_password': {'required': True},
            'is_teacher': {'required': True},
            'native_language': {'required': True},
            'target_language': {'required': True},

            'full_name': {'required': False},
            'zoom_access_token': {'required': False},
            'zoom_refresh_token': {'required': False},
            'zoom_token_expiration': {'required': False},
            'zoom_user_id': {'required': False},
            'is_zoom_authenticated': {'required': False},
        }


class MeetingRecordingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'meeting',
            'file_id',
            'file_name',
            'file_type',
            'file_size',
            'download_url',
            'download_token',
            'user'
        )
        model = MeetingRecordings

    def get_user(self, obj):
        file_name = obj.file_name
        user_name = Utils.extract_name(file_name)
        try:
            user = User.objects.get(full_name=user_name)
        except User.DoesNotExist:
            return None
        return user.uuid

    def validate(self, data):
        # Check if the file is already a recording
        if MeetingRecordings.objects.filter(meeting=data['meeting'], file_id=data['file_id']).exists():
            raise serializers.ValidationError("The file is already a recording of the meeting.")
        return data


class MeetingParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'uuid',
            'full_name',
            'email',
            'native_language',
            'target_language'
        )
        model = User


class MeetingSerializer(serializers.ModelSerializer):
    participants = MeetingParticipantsSerializer(read_only=True, many=True)
    meeting_recordings = MeetingRecordingSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            'uuid',
            'zoom_meeting_uuid',
            'start_time',
            'end_time',
            'host',
            'languages',
            'transcription_blob',
            'participants',
            'meeting_recordings',
        )
        model = Meeting
