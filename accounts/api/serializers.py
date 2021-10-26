from django.contrib.auth import get_user_model
from rest_framework import serializers
import datetime
#token payload handler
from rest_framework_jwt.settings import api_settings
from .utils import jwt_response_payload_handler
from django.utils import timezone

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

expires_Delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    #want to get url
    uri  = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri'
        ]
    def get_uri(self,obj):
        return "/api/user/{id}".format(id=obj.id)

class RegisterSerializer(serializers.ModelSerializer):
    #write_only is use for not show password in response
    password       = serializers.CharField(style={'input_type':'password'},write_only=True)
    password2      = serializers.CharField(style={'input_type':'password'},write_only=True)
    #serializer method
    token          = serializers.SerializerMethodField(read_only = True)
    expires        = serializers.SerializerMethodField(read_only = True)
    # token_response = serializers.SerializerMethodField(read_only = True)
    message        = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'token',
            'expires',
            # 'token_response'
            'message'
        ]
        extra_kwargs = {'password':{'write_only':True}}

    def get_message(self,obj):
        return "Thankyou for registrations."

    # def get_token_response(self,obj):
    #     user = obj
    #     payload = jwt_payload_handler(user)
    #     token  = jwt_encode_handler(payload)
    #     context = self.context
    #     request = context['request']
    #     print(request.user.is_authenticated)
    #     response = jwt_response_payload_handler(token,user,request=request)
    #     return response

    def get_expires(self,obj):
        return timezone.now() + expires_Delta + datetime.timedelta(seconds=200)

    def validate_email(self,value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with email already exists")
        return value

    def validate_username(self,value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with username already exists")
        return value

    def get_token(self,obj): # instance of the model
        user = obj
        payload = jwt_payload_handler(user)
        token  = jwt_encode_handler(payload)
        return token

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.get('password2')

        if pw != pw2:
            raise serializers.ValidationError("Password must be match.")
        # print(data)
        return data

    def create(self,validated_data):
        print(validated_data)
        user_obj = User(
            username = validated_data.get('username'),
            email = validated_data.get('email')
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = False
        user_obj.save()
        return user_obj
