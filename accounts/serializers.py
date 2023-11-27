from .models import Account
from rest_framework import serializers


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=8)

    class Meta:
        model = Account
        fields = ['username', 'password']


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=8)

    class Meta:
        model = Account
        fields = ['full_name']
