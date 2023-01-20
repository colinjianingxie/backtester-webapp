import uuid

from django.db import models

from .exchange import Exchange

class Symbol(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticker = models.CharField(max_length=32)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, blank=True, null=True)
    instrument = models.CharField(max_length=64)
    name = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=32, blank=True, null=True)
    created_date = models.DateTimeField("created date", auto_now_add=True)
    last_updated_date = models.DateTimeField("last updated date", auto_now=True)

    @property
    def get_latest_daily_price(self):
        return self.daily_price.all().order_by('-price_date').first()
    def __str__(self):
        return f"{self.ticker}"
