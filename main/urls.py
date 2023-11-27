from django.urls import path
from . import views

urlpatterns = [
    path('order-create/', views.OrderClientCreateAPIView.as_view()),
    path('order-file-create/', views.OrderClientFileCreateAPIView.as_view()),
    path('order/<int:pk>/', views.OrderClientRetrieveAPIView.as_view()),
    path('orders/', views.OrderClientListAPIView.as_view()),
    path('specialist-create/', views.SpecialistAPIView.as_view()),
    path('accountant/', views.AccountantListAPIView.as_view()),
    path('accountant/<int:pk>/', views.AccountantUpdateAPIView.as_view()),
    path('accountant/<int:pk>/', views.AccountantRetrieveAPIView.as_view()),
    path('statictics/', views.StatisticsAPIView.as_view()),
    path('inspector-1/', views.Inspector1UpdateAPIView.as_view()),
    path('inspector-2/', views.Inspector2UpdateAPIView.as_view()),
    path('product-list/', views.ProductListAPIView.as_view()),
    path('product-create/', views.ProductCreateAPIView.as_view())
]
