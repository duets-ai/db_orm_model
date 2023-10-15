from rest_framework import serializers
from .models import *
import re


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
            'transcription_id',
            'host',
            'participants',
            'meeting_recordings'
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


def extract_name(s):
    match = re.search(r'Audio only - (\w+ \w+)', s)
    return match.group(1) if match else None


class MeetingRecordingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = MeetingRecordings
        fields = ['meeting', 'file_id', 'file_name', 'file_type', 'file_size', 'download_url', 'download_token', 'user']

    def get_user(self, obj):
        file_name = obj.file_name
        user_name = extract_name(file_name)
        user = User.objects.get(full_name=user_name)
        return ParticipantSerializer(user).data

    def validate(self, data):
        # Check if the file is already a recording
        if MeetingRecordings.objects.filter(meeting=data['meeting'], file_id=data['file_id']).exists():
            raise serializers.ValidationError("The file is already a recording of the meeting.")
        return data


class TranscriptionSerializer(serializers.ModelSerializer):
    transcripts = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'uuid',
            'meeting_uuid',
            'transcripts',
        )
        model = Transcription

    def get_transcripts(self, obj):
        all_transcripts = TranscriptionElement.objects.filter(meeting_uuid=obj.meeting_uuid)
        transcript_dict = {}

        for transcript in all_transcripts:
            speaker_uuid = transcript.speaker_uuid
            if speaker_uuid not in transcript_dict:
                transcript_dict[speaker_uuid] = []
            transcript_data = {
                'text': transcript.text,
                'start': transcript.start,
                'end': transcript.end
            }
            transcript_dict[speaker_uuid].append(transcript_data)
        return transcript_dict


class TranscriptionElementSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'transcription_uuid',
            'speaker_uuid',
            'text',
            'start',
            'end',
        )
        model = TranscriptionElement

    def validate(self, data):
        # Check if the transcript is already in the database
        if TranscriptionElement.objects.filter(transcription_uuid=data['transcription_uuid'], text=data['text'],
                                               start=data['start'], end=data['end']).exists():
            raise serializers.ValidationError("The transcript is already in the database.")
        return data
