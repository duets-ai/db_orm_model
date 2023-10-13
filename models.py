import uuid
from django.db import models


class User(models.Model):
    uuid = models.CharField(max_length=128, unique=True, default=uuid.uuid4, primary_key=True)
    native_language = models.CharField(max_length=50, blank=True)
    target_language = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    is_teacher = models.BooleanField(default=False)
    zoom_access_token = models.CharField(max_length=800)
    zoom_refresh_token = models.CharField(max_length=800)
    zoom_token_expiration = models.CharField(max_length=512)
    zoom_user_id = models.CharField(max_length=50)
    is_zoom_authenticated = models.BooleanField(default=False)


class Meeting(models.Model):
    uuid = models.CharField(max_length=128, unique=True, default=uuid.uuid4, primary_key=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    zoom_meeting_uuid = models.CharField(max_length=50)
    transcription_id = models.CharField(max_length=50, blank=True)
    host = models.CharField(max_length=128)


class MeetingParticipants(models.Model):
    meeting = models.CharField(max_length=128)  # UUID of the Meeting
    user = models.CharField(max_length=128)  # UUID of the User

    class Meta:
        unique_together = ['meeting', 'user']


class MeetingRecordings(models.Model):
    meeting = models.CharField(max_length=128)  # UUID of the Meeting
    file_id = models.CharField(max_length=50)  # UUID of the Recording
    file_name = models.CharField(max_length=128)
    file_type = models.CharField(max_length=128)
    file_size = models.IntegerField()
    download_url = models.CharField(max_length=512)
    download_token = models.CharField(max_length=512)

    class Meta:
        unique_together = ['meeting', 'file_id']


class Transcription(models.Model):
    uuid = models.CharField(max_length=50, unique=True, default=uuid.uuid4, primary_key=True)
    meeting_uuid = models.CharField(max_length=128)  # UUID of the Meeting


class TranscriptionElement(models.Model):
    transcription_uuid = models.CharField(max_length=50)  # UUID of the Transcription
    speaker_uuid = models.CharField(max_length=128)  # UUID of the User
    text = models.TextField()
    start = models.IntegerField()
    end = models.IntegerField()

    class Meta:
        unique_together = ['meeting_uuid', 'speaker_uuid', 'start', 'end']
