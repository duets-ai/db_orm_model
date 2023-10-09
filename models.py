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
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    zoom_meeting_uuid = models.CharField(max_length=50)
    transcription_id = models.CharField(max_length=50)
