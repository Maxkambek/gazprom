import datetime
from rest_framework.settings import api_settings
from accounts.models import Account
from .models import Product, OrderClient, OrderClientFile, OrderClientProducts
from rest_framework import generics, authentication, permissions
from rest_framework.views import Response, status, APIView
from . import serializers
from accounts.utils import verify


class OrderClientFileCreateAPIView(generics.CreateAPIView):
    queryset = OrderClientFile.objects.all()
    serializer_class = serializers.OrderClientFileSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class OrderClientCreateAPIView(generics.CreateAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.OrderClientCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
        phone = serializer.data['phone']
        id = serializer.data['id']
        try:
            user = Account.objects.create(
                username=phone,
                password="12345678"
            )
            user.save()
            verify(phone)
        except:
            obj = OrderClient.objects.filter(id=id).first()
            obj.client.username = phone

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class OrderClientListAPIView(generics.ListAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.OrderClientListSerializer


class OrderClientRetrieveAPIView(generics.RetrieveAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.OrderClientListSerializer


class Inspector1UpdateAPIView(generics.UpdateAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.Inspector1Serializer


class Inspector2UpdateAPIView(generics.UpdateAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.Inspector2Serializer


class SpecialistAPIView(generics.CreateAPIView):
    queryset = OrderClientProducts.objects.all()
    serializer_class = serializers.SpecialistSerializer


class AccountantListAPIView(generics.ListAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.AccountantSerializer


class AccountantRetrieveAPIView(generics.RetrieveAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.AccountantSerializer


class AccountantUpdateAPIView(generics.UpdateAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.AccountantUpdateSerializer


class StatisticsAPIView(APIView):
    def get(self, request):
        queryset = OrderClient.objects.all()
        today = self.request.GET.get('today')
        yesterday = self.request.GET.get('yesterday')
        week = self.request.GET.get('week')
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        if today:
            queryset = queryset.filter(created_time__day=datetime.datetime.now().day)
        if yesterday:
            queryset = queryset.filter(created_time__day=datetime.datetime.now().day - 1)
        if week:
            queryset = queryset.filter(
                created_time__range=[datetime.datetime.now() - datetime.timedelta(days=7), datetime.datetime.now()])
        if month:
            queryset = queryset.filter(created_time__month=datetime.datetime.now().month)
        if year:
            queryset = queryset.filter(created_time__year=datetime.datetime.now().year)
        data = {
            'received': queryset.filter(status='received').count(),
            'specialist': queryset.filter(status='specialist').count(),
            'accountant': queryset.filter(status='accountant').count(),
            'payment': queryset.filter(status='payment').count(),
            'test': queryset.filter(status='test').count(),
            'docs': queryset.filter(status='docs').count(),
            'end': queryset.filter(status='end').count(),
        }
        return Response(data, status=200)
