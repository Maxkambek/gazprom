from .models import Account
from rest_framework import serializers


class HistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        return super().to_representation(data.values())


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=8)

    class Meta:
        model = Account
        fields = ['username', 'password']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'password']


class AccountSerializer(serializers.ModelSerializer):
    history = HistoricalRecordField(read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'full_name', 'role', 'username', 'history')
