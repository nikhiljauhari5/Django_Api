import datetime
from django.conf import settings
from django.utils import timezone
from rest_framework_jwt.settings import api_settings

expires_Delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA

# JWT_REFRESH_EXPIRATION_DELTA

# expires_Delta = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']
#get token with username when we want token
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user.username,
        'expires':timezone.now() + expires_Delta + datetime.timedelta(seconds=200)
    }
