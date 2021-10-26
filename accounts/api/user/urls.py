from django.urls import path,include
from rest_framework_jwt.views import refresh_jwt_token,obtain_jwt_token
from .views import UserDetailAPIView

urlpatterns =[
    path('detail/<pk>',UserDetailAPIView.as_view()),
]
