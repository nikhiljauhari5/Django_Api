from django.urls import path,include
from rest_framework_jwt.views import refresh_jwt_token,obtain_jwt_token
from .views import AuthView,RegisterView,RegisterAPIView
urlpatterns =[
    path('',AuthView.as_view()),
    path('register/',RegisterView.as_view()),
    path('register2/',RegisterAPIView.as_view()),
    path('jwt/',obtain_jwt_token),
    path('jwt/refresh/',refresh_jwt_token)
]
