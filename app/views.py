from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Status
from .serializers import StatusSerializer
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets,mixins,generics

from accounts.api.permissions import IsOwnerOrReadOnly
# Create your views here.

class StatusListAPIView(APIView):
    # permission_classes          = [IsAuthenticatedOrReadOnly]
    # permission_classes          = [IsOwnerOrReadOnly] #only owner is allow to change the thing and the AnonymousUser is only read this
    # authentication_classess     = [SessionAuthentication]
    search_fields               =  ('content','user__username')

    def get(self,request):
        qs = Status.objects.all()
        print(request.user)
        serialize = StatusSerializer(qs,many=True)
        data = serialize.data
        return Response(data)


#login required mixin and decorator
class StatusMixinsAPIView(mixins.CreateModelMixin,
            mixins.DestroyModelMixin,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,generics.ListAPIView):
    #IsAuthenticated = use for user must be login ot see and add the data
    #IsAuthenticatedOrReadOnly = use for read only permission
    # permission_classes          = [IsAuthenticatedOrReadOnly] # u aslo authenticate by oath and JWT
    # permission_classes          = [IsOwnerOrReadOnly]
    # authentication_classess     = [SessionAuthentication]
    serializer_class = StatusSerializer
    search_fields               =  ('content','user__username')

    def get_queryset(self):
        qs = Status.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontain=query)
        return qs

    def get_object(self):
        request = self.request
        passed_id = request.GET.get('id',None)
        queryset = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset,id=passed_id)
            self.check_object_permissions(request,obj)
        return obj

    # perform delete operations
    def perform_destroy(self,instance):
        if instance is not None:
            return instance.delete()
        return None

    def get(self,request,*args,**kwargs):
        passed_id = request.GET.get('id',None)
        print(request.user)
        if passed_id is not None:
            return self.retrieve(request,*args,**kwargs)
        return super().get(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request, *args, **kwargs)

    # if we do in serializer file user is only read_only then that
    # case we need to right this perform_create() func it takes by default
    # user existing instance.
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self,request,*args,**kwargs):
        passed_id = request.GET.get('id',None)
        print(request.user)
        if passed_id is not None:
            return self.update(request,*args,**kwargs)
        return self.update(request, *args, **kwargs)

    def patch(self,request,*args,**kwargs):
        return self.update(request, *args, **kwargs)

class StatusAPIView(viewsets.ModelViewSet):
    # permission_classes          = []
    # authentication_classes     = []
    queryset  = Status.objects.all()
    serializer_class = StatusSerializer
    search_fields               = ('content','user__username')
    #query filterations in viewsets
    def get_queryset(self):
        qs = Status.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontain=query)
        return qs

#serializer with single object
#
# obj = Status.objects.first()
# data = StatusSerializer(obj)
# data.is_valid()
# data.save()
# data.data


#serializer with single object
#
# obj = Status.objects.all()
# data = StatusSerializer(obj,many=True)
# data.is_valid()
# data.save()
# data.data

#create data with serializer

# data = {'user':1,'content':"some new content",'image':''}
# data = StatusSerializer(data=data)
# data.is_valid()
# data.save()

#update data with serializer

# obj = Status.objects.first()
# data = {'user':1,'content':"some new content"}
# data = StatusSerializer(obj,data=data)
# data.is_valid()
# data.save()

#delete data with serializer

# obj = Status.objects.filter(id=1)
# obj.delete()
