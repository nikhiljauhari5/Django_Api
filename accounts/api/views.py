from django.contrib.auth import authenticate,get_user_model
from django.db.models import  Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings
from .utils import jwt_response_payload_handler

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


#custom user  get_user_model
User = get_user_model()

class AuthView(APIView):
    permission_classes          = [AllowAny]
    authentication_classess     = []

    def post(self,request,*args,**kwargs):
        print(request.user)
        if request.user.is_authenticated:
            return Response({'detail':'you are already authenticated'},status=400)
        data = request.data
        username = data.get('username') #username or email address validation
        password = data.get('password')
        user = authenticate(username=username,password=password)
        print(user)

        # its use when we authenticate the email address or user
        qs = User.objects.filter(
            Q(username__iexact=username)|
            Q(email__iexact=username)
        ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token  = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token,user,request=request)
                return Response(response)
        return Response({"detail":"Invalid credentials"},status=401)

        # payload = jwt_payload_handler(user)
        # token = jwt_encode_handler(payload)
        # response = jwt_response_payload_handler(token,user,request=request)
        #
        # return Response(response)


#this is also done by serializer please check serializers.py file in api after this view

class RegisterView(APIView):
    permission_classes          = [AllowAny]
    authentication_classess     = []

    def post(self,request,*args,**kwargs):
        print(request.user)
        if request.user.is_authenticated:
            return Response({'detail':'you are already authenticated'},status=400)
        data = request.data
        username     = data.get('username') #username or email address validation
        email        = data.get('username')
        password     = data.get('password')
        password2    = data.get('password2')
        qs = User.objects.filter(
            Q(username__iexact=username)|
            Q(email__iexact=username)
        )
        if password != password2:
            return Response({'password':'password must match.'},status=401)
        if qs.exists():
            return Response({'detail':'you are already exists'},status=401)
        else:
            user = User.objects.create(username=username,email=email)
            user.set_password(password)
            user.save()
            print(user)
            payload = jwt_payload_handler(user)
            token  = jwt_encode_handler(payload)
            response = jwt_response_payload_handler(token,user,request=request)
            # return Response(response,status=201) #this is returning the token and there data
            return Response({'detail':'thankyou for registering. Please verify your email.'},status=201)
        return Response({"detail":"Invalid Request"},status=400)

from .serializers import RegisterSerializer
from rest_framework import generics,mixins
from .permissions import AnonPermissionOnly,IsOwnerOrReadOnly

class RegisterAPIView(generics.CreateAPIView):
    queryset                = User.objects.all()
    serializer_class        = RegisterSerializer
    # permission_classes      = [AllowAny]
    # permission_classes      = [AnonPermissionOnly]
    permission_classes      = [IsOwnerOrReadOnly] # do not update data without permission of owner

    def get_serializer_context(self,*args,**kwargs):
        return {"request":self.request}
