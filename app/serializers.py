from rest_framework import serializers

from .models import Status
from accounts.api.serializers import UserPublicSerializer
'''
serializer = Json
serializer = validate data
'''

# class CustomSerializer(serializers.ModelSerializer):
#     content = serializer.CharField()
#     email = serializer.EmailField()


#this serializer user for reverse relation in api.user.serializer
class StatusInlineUserSerializer(serializers.ModelSerializer):
    uri  = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Status
        fields = [
            'id',
            'content',
            'uri',
            'image'
        ]
    def get_uri(self,obj):
        return "/api/user/{id}".format(id=obj.id)


class StatusSerializer(serializers.ModelSerializer):
    uri  = serializers.SerializerMethodField(read_only=True)
    user = UserPublicSerializer(read_only=True) #nested serializer
    class Meta:
        model = Status
        fields = [
            'id',
            'user',
            'content',
            'uri',
            'image'
        ]
        read_only_fields = ['user']
    def get_uri(self,obj):
        return "/api/user/{id}".format(id=obj.id)

    def validate_content(self,value):
        if len(value) < 10:
            raise serializers.ValidationError("content are too short")
        return value

    def validate(self,data):
        content = data.get('content',None)
        if content == "":
            content = None
        image = data.get('image',None)
        if content is None and image is None:
            raise serializers.ValidationError("content or image is required")
        return data
