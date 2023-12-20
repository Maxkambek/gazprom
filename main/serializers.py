from rest_framework import serializers
from .models import Product, OrderClient, OrderClientFile, OrderClientProducts, UzStandard


class UzStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UzStandard
        fields = ['file_1', 'file_2', 'file_3', 'order']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'number_hash', 'count', 'come_time', 'price']


class OrderClientProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderClientProducts
        fields = ['id', 'order', 'product', 'count']


class OrderClientFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderClientFile
        fields = ['file', 'order']


class OrderClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderClient
        fields = ['id', 'name_org', 'created_time', 'status', 'meter_brand', 'serial_number', 'temp_sensor',
                  'latest_certificate', 'passport_meter', 'correction_block_passport', 'verification_with_stamp',
                  'gaz_pribor_stamp', 'block_correction_dp', 'dt', 'dd', 'er_300000', 'visual_damage',
                  'mechanical_damage', 'conclusion', 'indications', 'counting_mechanism', 'phone',
                  'is_checked', 'is_paid']


class OrderClientListSerializer(serializers.ModelSerializer):
    order_products = OrderClientProductsSerializer(many=True)

    class Meta:
        model = OrderClient
        fields = ['id', 'name_org', 'created_time', 'status', 'meter_brand', 'serial_number', 'temp_sensor',
                  'latest_certificate', 'passport_meter', 'correction_block_passport', 'verification_with_stamp',
                  'gaz_pribor_stamp', 'block_correction_dp', 'dt', 'dd', 'er_300000', 'visual_damage',
                  'mechanical_damage', 'conclusion', 'indications', 'counting_mechanism', 'phone', 'client',
                  'is_checked', 'is_paid', 'order_products', 'get_full_amount']


class OrderClientListForUzSerializer(serializers.ModelSerializer):
    order_files = OrderClientFileSerializer(many=True)

    class Meta:
        model = OrderClient
        fields = ['id', 'name_org', 'created_time', 'meter_brand', 'serial_number', 'temp_sensor',
                  'latest_certificate', 'passport_meter', 'correction_block_passport', 'verification_with_stamp',
                  'gaz_pribor_stamp', 'block_correction_dp', 'dt', 'dd', 'er_300000', 'visual_damage',
                  'mechanical_damage', 'conclusion', 'indications', 'counting_mechanism', 'order_files']


class Inspector1Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderClient
        fields = ['id', 'is_checked']


class Inspector2Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderClient
        fields = ['id', 'is_available']


class SpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderClientProducts
        fields = ['id', 'order', 'product', 'count']


class AccountantSerializer(serializers.ModelSerializer):
    order_files = OrderClientFileSerializer(many=True)
    order_products = OrderClientProductsSerializer(many=True)

    class Meta:
        model = OrderClient
        fields = ['id', 'name_org', 'created_time', 'status', 'meter_brand', 'serial_number', 'temp_sensor',
                  'latest_certificate', 'passport_meter', 'correction_block_passport', 'verification_with_stamp',
                  'gaz_pribor_stamp', 'block_correction_dp', 'dt', 'dd', 'er_300000', 'visual_damage',
                  'mechanical_damage', 'conclusion', 'indications', 'counting_mechanism', 'phone', 'client',
                  'is_checked', 'is_paid', 'order_files', 'order_products', 'get_full_amount']


class AccountantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderClient
        fields = ['id', 'ready_for_paid']


class Specialist2Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderClient
        fields = ['id', 'status']


class Receiver2Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderClient
        fields = ['id', 'is_paid', 'status']
