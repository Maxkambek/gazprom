import datetime
from rest_framework.settings import api_settings
from accounts.models import Account
from .models import Product, OrderClient, OrderClientFile, OrderClientProducts, UzStandard
from rest_framework import generics, authentication, permissions
from rest_framework.views import Response, status, APIView
from . import serializers
from accounts.utils import verify
from .serializers import OrderClientListSerializer, OrderClientListForUzSerializer
from django.utils import timezone
from datetime import timedelta


# uz standard
class UzStandardCreateAPIView(generics.CreateAPIView):
    queryset = UzStandard.objects.all()
    serializer_class = serializers.UzStandardSerializer


# receiver
class OrderClientFileCreateAPIView(generics.CreateAPIView):
    queryset = OrderClientFile.objects.all()
    serializer_class = serializers.OrderClientFileSerializer


# accountant
class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


# specialist accountant
class ProductListAPIView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class ProductRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()


# receiver
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
        order_id = serializer.data['id']
        user = Account.objects.filter(username=phone).first()
        if not user:
            user = Account.objects.create(
                username=phone,
                password="12345678",
                role="client",
                is_active=True
            )
            user.save()
            verify(phone)
        obj = OrderClient.objects.filter(id=order_id).first()
        obj.status = 'specialist'
        obj.level_order = 2
        obj.client = user
        obj.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


# receiver
class OrderClientListAPIView(generics.ListAPIView):
    serializer_class = serializers.OrderClientListSerializer

    def get_queryset(self):
        queryset = OrderClient.objects.all().order_by("-id")
        today = self.request.GET.get('today')
        yesterday = self.request.GET.get('yesterday')
        week = self.request.GET.get('week')
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        if today:
            queryset = queryset.filter(created_time__day=timezone.now().day)
        if yesterday:
            queryset = queryset.filter(created_time__day=timezone.now().day - 1)
        if week:
            print(datetime.datetime.now() - datetime.timedelta(days=7))
            queryset = queryset.filter(
                created_time__range=[timezone.now() - timedelta(days=7), timezone.now()])
        if month:
            queryset = queryset.filter(created_time__month=timezone.now().month)
        if year:
            queryset = queryset.filter(created_time__year=timezone.now().year)
        return queryset


# receiver
class OrderClientForEndListAPIView(generics.ListAPIView):
    serializer_class = serializers.OrderClientListSerializer

    def get_queryset(self):
        queryset = OrderClient.objects.all().order_by('-id')
        return queryset


# specialist
class OrderClientSpecialistListAPIView(generics.ListAPIView):
    serializer_class = serializers.OrderClientListSerializer

    def get_queryset(self):
        queryset = OrderClient.objects.filter(status='specialist').order_by("-id")
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
        return queryset


# specialist
class OrderClientRetrieveAPIView(generics.RetrieveAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.OrderClientListSerializer


# specialist
class SpecialistCreateAPIView(generics.CreateAPIView):
    queryset = OrderClientProducts.objects.all()
    serializer_class = serializers.SpecialistSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        order_id = serializer.data['order']
        order = OrderClient.objects.get(id=order_id)
        order.level_order = 3
        order.status = 'accountant'
        order.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


# Accountant
class AccountantListAPIView(generics.ListAPIView):
    serializer_class = serializers.AccountantSerializer

    def get_queryset(self):
        queryset = OrderClient.objects.filter(status="accountant").order_by("-id")
        today = self.request.GET.get('today')
        yesterday = self.request.GET.get('yesterday')
        if today:
            queryset = queryset.filter(created_time__day=datetime.datetime.now().day)
        if yesterday:
            queryset = queryset.filter(created_time__day=datetime.datetime.now().day - 1)
        return queryset


# accountant
class AccountantUpdateAPIView(generics.UpdateAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.AccountantUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.status = 'payment'
        instance.level_order = 4
        instance.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


# Statistics
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


# inspectors


class Inspector1UpdateAPIView(generics.UpdateAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.Inspector1Serializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.inspector_1 = True
        instance.level_order += 1
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class Inspector2UpdateAPIView(generics.UpdateAPIView):
    queryset = OrderClient.objects.all()
    serializer_class = serializers.Inspector2Serializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.inspector_2 = True
        instance.status = 'specialist'
        instance.level_order += 1
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class OrderClientInstructor1ListAPIView(generics.ListAPIView):
    serializer_class = serializers.OrderClientListSerializer

    def get_queryset(self):
        queryset = OrderClient.objects.filter(is_paid=True, inspector_1=False).order_by("-id")
        today = self.request.GET.get('today')
        yesterday = self.request.GET.get('yesterday')
        if today:
            queryset = queryset.filter(created_time__day=datetime.datetime.now().day)
        if yesterday:
            queryset = queryset.filter(created_time__day=datetime.datetime.now().day - 1)
        return queryset


class OrderClientInstructor2ListAPIView(generics.ListAPIView):
    serializer_class = serializers.OrderClientListSerializer

    def get_queryset(self):
        queryset = OrderClient.objects.filter(is_paid=True, inspector_2=False, is_checked=False,
                                              inspector_1=True).order_by("-id")
        today = self.request.GET.get('today')
        yesterday = self.request.GET.get('yesterday')
        if today:
            queryset = queryset.filter(created_time__day=datetime.datetime.now().day)
        if yesterday:
            queryset = queryset.filter(created_time__day=datetime.datetime.now().day - 1)
        return queryset


# client
class ClientListAPIView(generics.ListAPIView):
    serializer_class = OrderClientListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        qs = OrderClient.objects.filter(client_id=self.request.user.id)
        return qs


# uz standard
class UzStandardListAPIView(generics.ListAPIView):
    serializer_class = OrderClientListForUzSerializer

    def get_queryset(self):
        qs = OrderClient.objects.filter(status='docs')
        return qs


# specialist 2
class Specialist2ListAPIView(generics.ListAPIView):
    serializer_class = serializers.OrderClientListSerializer
    queryset = OrderClient.objects.filter(status="specialist_2")


class SpecialistUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.Specialist2Serializer
    queryset = OrderClient.objects.all()


class Reciever2UpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.Receiver2Serializer
    queryset = OrderClient.objects.all()
