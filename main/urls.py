from django.urls import path
from . import views

urlpatterns = [
    # receive
    path('order-create/', views.OrderClientCreateAPIView.as_view()),
    path('order-file-create/', views.OrderClientFileCreateAPIView.as_view()),
    path('order/<int:pk>/', views.OrderClientRetrieveAPIView.as_view()),
    path('orders/', views.OrderClientListAPIView.as_view()),
    path('orders-history/', views.OrderClientForEndListAPIView.as_view()),
    # specialist
    path('orders-specialist/', views.OrderClientSpecialistListAPIView.as_view()),
    path('specialist-create/', views.SpecialistCreateAPIView.as_view()),
    path('product-list/', views.ProductListAPIView.as_view()),
    path('product-create/', views.ProductCreateAPIView.as_view()),
    # accountant
    path('accountant/', views.AccountantListAPIView.as_view()),
    path('accountant/<int:pk>/', views.AccountantUpdateAPIView.as_view()),
    path('statictics/', views.StatisticsAPIView.as_view()),
    # inspector
    path('inspector1-order-list/', views.OrderClientInstructor1ListAPIView.as_view()),
    path('inspector2-order-list/', views.OrderClientInstructor2ListAPIView.as_view()),
    path('inspector-1/<int:pk>/', views.Inspector1UpdateAPIView.as_view()),
    path('inspector-2/<int:pk>/', views.Inspector2UpdateAPIView.as_view()),
    path('uz-standard/', views.UzStandardCreateAPIView.as_view()),
    path('client/', views.ClientListAPIView.as_view()),
    path('list-for-uzstandard/', views.UzStandardListAPIView.as_view()),
]
