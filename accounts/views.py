from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Account
from .serializers import LoginSerializer, AccountSerializer, RegisterSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from hashlib import sha1
import hashlib

hash_algorithm = 'sha256'


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data['username']
        pas = request.data['password']
        user = Account.objects.filter(username=username, password=pas).first()
        print(user)
        if not user:
            return Response({'message': 'Bunaqa user yogu nima qilamiza endi'}, status=status.HTTP_404_NOT_FOUND)
        token = Token.objects.get_or_create(user=user)
        data = dict()
        data['token'] = str(token)
        data['success'] = True
        data['role'] = user.role
        if user.full_name:
            data['name'] = user.full_name
        return Response(data, status=status.HTTP_200_OK)


class WorkersList(generics.ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = Account.objects.filter(is_staff=True)
        return queryset


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        username = self.request.data['username']
        pas = request.data['password']
        role = request.data['role']
        name = request.data['full_name']
        if not username:
            return Response({'Telefon raqam kemadi tupoymisz?'}, status=404)
        if Account.objects.filter(username=username).first():
            return Response({'message': "This number already exist"}, status=status.HTTP_302_FOUND)
        user = Account.objects.create(
            username=username,
            password=pas,
            is_active=True,
            role=role,
            full_name=name
        )
        user.save()
        print(user)
        return Response({"success": True, 'message': "User created"},
                        status=status.HTTP_200_OK)


class StaffListAPIView(generics.ListAPIView):
    queryset = Account.objects.filter(is_staff=True)
    serializer_class = AccountSerializer
