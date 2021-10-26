from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()
from app.serializers import StatusInlineUserSerializer

class UserDetailSerializer(serializers.ModelSerializer):
    #want to get url
    uri          = serializers.SerializerMethodField(read_only=True)
    status_list  = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri',
            'status_list'
        ]
    def get_uri(self,obj):
        return "/api/user/{id}".format(id=obj.id)

    def get_status_list(self,obj):
        # qs = obj.status_set.all() # filter status.objects.filter(user=obj)
        #this qs for orderby
        qs = obj.status_set.all().order_by("-timestamp")[:10]
        return StatusInlineUserSerializer(qs,many=True).data
