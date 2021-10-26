from django.contrib.auth import authenticate,get_user_model
from .serializers import UserDetailSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets,mixins,generics,pagination
#custom user  get_user_model
from app.models import Status
from app.serializers import StatusInlineUserSerializer

User = get_user_model()

class CustomPagination(pagination.PageNumberPagination):
    page_size = 2


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset                = User.objects.filter(is_active=True)
    serializer_class        = UserDetailSerializer
    permission_classes      = [IsAuthenticatedOrReadOnly]
    #pagination only apply on List not Retrieve
    pagination_class        = CustomPagination
    lockup_field            = 'pk'
