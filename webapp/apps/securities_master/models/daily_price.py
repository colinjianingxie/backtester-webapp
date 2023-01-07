import uuid
from django.db import models
from .data_vendor import DataVendor
from .symbol import Symbol

class DailyPrice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    data_vendor = models.ForeignKey(DataVendor, on_delete=models.CASCADE, blank=True, null=True)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    price_date = models.DateTimeField("price date")
    created_date = models.DateTimeField("created date", auto_now_add=True)
    last_updated_date = models.DateTimeField("last updated date", auto_now=True)
    open_price = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    high_price = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    low_price = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    close_price = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    adj_close_price = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.symbol}"
