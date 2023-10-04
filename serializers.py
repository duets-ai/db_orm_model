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