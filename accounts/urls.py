from .views import LoginAPI, RegisterAPI
from django.urls import path

urlpatterns = [
    path('login/', LoginAPI.as_view()),
    path('register/', RegisterAPI.as_view()),
]
