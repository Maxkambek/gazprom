from django.db import models
from accounts.models import Account


class Product(models.Model):
    name = models.CharField(max_length=333)
    number_hash = models.CharField(max_length=123)
    count = models.PositiveIntegerField(default=0)
    come_time = models.CharField(max_length=123)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


STATUS = (
    ("received", "received"),
    ("specialist", "specialist"),
    ("accountant", "accountant"),
    ('payment', 'payment'),
    ("specialist_2", "specialist_2"),
    ("test", "test"),
    ("docs", "docs"),
    ("end", "end"),
)


class OrderClient(models.Model):
    is_paid = models.BooleanField(default=False)
    name_org = models.CharField(max_length=333)
    created_time = models.DateTimeField()
    status = models.CharField(max_length=123, choices=STATUS, default='received')
    meter_brand = models.CharField(max_length=123)
    serial_number = models.CharField(max_length=123)
    temp_sensor = models.CharField(max_length=123)
    latest_certificate = models.BooleanField(default=False)
    passport_meter = models.BooleanField(default=False)
    correction_block_passport = models.BooleanField(default=False)
    verification_with_stamp = models.BooleanField(default=False)
    gaz_pribor_stamp = models.BooleanField(default=False)
    block_correction_dp = models.BooleanField(default=False)
    dt = models.BooleanField(default=False)
    dd = models.BooleanField(default=False)
    er_300000 = models.BooleanField(default=False)
    visual_damage = models.BooleanField(default=False)
    mechanical_damage = models.BooleanField(default=False)
    conclusion = models.TextField()
    indications = models.TextField()
    counting_mechanism = models.TextField()
    phone = models.CharField(max_length=20)
    client = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    is_checked = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    ready_for_paid = models.BooleanField(default=False)
    level_order = models.PositiveIntegerField(default=1)
    inspector_1 = models.BooleanField(default=False)
    inspector_2 = models.BooleanField(default=False)

    def __str__(self):
        return self.name_org

    @property
    def get_full_amount(self):
        amount = 0
        for i in self.order_products.all():
            amount += i.product.price * i.count
        return amount


class OrderClientFile(models.Model):
    file = models.FileField(upload_to='files/')
    order = models.ForeignKey(OrderClient, on_delete=models.CASCADE, related_name='order_files')

    def __str__(self):
        return self.order.name_org


class OrderClientProducts(models.Model):
    order = models.ForeignKey(OrderClient, on_delete=models.SET_NULL, null=True, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_product')
    count = models.PositiveIntegerField(default=1)


class UzStandard(models.Model):
    file_1 = models.FileField(upload_to='uz_standard/')
    file_2 = models.FileField(upload_to='uz_standard/', null=True, blank=True)
    file_3 = models.FileField(upload_to='uz_standard/', null=True, blank=True)
    order = models.ForeignKey(OrderClient, on_delete=models.CASCADE, related_name='uaz_standard_files')

    def __str__(self):
        return self.order.name_org
