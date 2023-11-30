from .views import LoginAPI, RegisterAPI, StaffListAPIView
from django.urls import path

urlpatterns = [
    path('login/', LoginAPI.as_view()),
    path('register/', RegisterAPI.as_view()),
    path('staff/', StaffListAPIView.as_view())
]
