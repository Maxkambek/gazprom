from django.urls import path
from . import views

urlpatterns = [
    path('card-create/', views.CardCreate.as_view()),
    path('verify-phone/', views.CardVerify.as_view()),
    path('payment/', views.ReceiptCreate.as_view()),
]