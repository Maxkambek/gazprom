from django.db import models
from accounts.models import Account


class Order(models.Model):
    client = models.ForeignKey(Account, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'
