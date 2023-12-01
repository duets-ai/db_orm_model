import uuid
from django.db import models


class User(models.Model):

    #Frontend Auth Fields
    uuid = models.CharField(max_length=128, unique=True, default=uuid.uuid4, primary_key=True)
    email = models.EmailField(max_length=50)
    hashed_password = models.CharField(max_length=50)

    #Zoom Auth Fields
    full_name = models.CharField(max_length=50)
    zoom_access_token = models.CharField(max_length=800)
    zoom_refresh_token = models.CharField(max_length=800)
    zoom_token_expiration = models.CharField(max_length=512)
    zoom_user_id = models.CharField(max_length=50)
    is_zoom_authenticated = models.BooleanField(default=False)

    #User Profile Fields
    native_language = models.CharField(max_length=50, blank=True)
    target_language = models.CharField(max_length=50, blank=True)
    is_teacher = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'


class MeetingRecordings(models.Model):
    uuid = models.CharField(max_length=128, unique=True, default=uuid.uuid4, primary_key=True)
    meeting = models.CharField(max_length=128)  # UUID of the Meeting
    file_id = models.CharField(max_length=50)
    file_name = models.CharField(max_length=128)
    file_type = models.CharField(max_length=128)
    file_size = models.IntegerField()
    download_url = models.CharField(max_length=512)
    download_token = models.CharField(max_length=512)

    class Meta:
        unique_together = ['meeting', 'file_id']
        db_table = 'meeting_recordings'


class Meeting(models.Model):
    uuid = models.CharField(max_length=128, unique=True, default=uuid.uuid4, primary_key=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    zoom_meeting_uuid = models.CharField(max_length=50)
    host = models.CharField(max_length=128)
    languages = models.JSONField(default=list, blank=True)
    transcription_blob = models.CharField(max_length=256, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    meeting_recordings = models.ManyToManyField(MeetingRecordings, related_name='meeting_recordings', blank=True)
    feedback_blob = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = 'meetings'
